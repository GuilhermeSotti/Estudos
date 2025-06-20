import argparse
import logging
import os
from src.config import load_config
from src.logger import setup_logging
from src.data_loading import load_seeds_raw, save_processed_df
from src.preprocessing import check_missing, handle_outliers, split_data, fit_scaler, save_scaler
from src.feature_engineering import calc_compactness, calc_ratio_length_width
from src.modeling import build_pipeline, cross_validate_model
from src.tuning import tune_model
from src.evaluation import evaluate_model
import joblib
from sklearn.model_selection import StratifiedKFold

def main():
    parser = argparse.ArgumentParser(description="Treina e otimiza modelos para Seeds Dataset")
    parser.add_argument("--config", type=str, required=False, help="Caminho para arquivo YAML de configuração", default="Cap 3 - (IR ALÉM) Implementando algoritmos de Machine Learning com Scikit-learn\config\default.yaml")
    args = parser.parse_args()
    cfg = load_config(args.config)

    setup_logging(cfg.output.log_dir, cfg.logging.get("level", "INFO"))
    logger = logging.getLogger(__name__)
    logger.info("Iniciando processo de treino")

    df = load_seeds_raw(cfg.data.raw_path)
    miss = check_missing(df)
    logger.info(f"Missing por coluna:\n{miss}")

    df = handle_outliers(df, columns=['area','perimeter','length','width','asymmetry','groove'])

    feature_cols = ['area','perimeter']
    if cfg.features.use_compactness:
        df = calc_compactness(df, area_col='area', perim_col='perimeter', out_col='compactness_calc')
        feature_cols.append('compactness_calc')
    if cfg.features.use_ratio_length_width:
        df = calc_ratio_length_width(df, length_col='length', width_col='width', out_col='ratio_length_width')
        feature_cols.append('ratio_length_width')

    for col in ['length','width','asymmetry','groove']:
        feature_cols.append(col)

    X_train, X_test, y_train, y_test = split_data(df, feature_cols, 'class', cfg.data.test_size, cfg.data.random_state, stratify=cfg.data.stratify)

    cv = StratifiedKFold(n_splits=cfg.model.cv_n_splits, shuffle=cfg.model.cv_shuffle, random_state=cfg.data.random_state)
    best_model = None
    best_score = -float('inf')
    best_name = ""

    for cand in cfg.model.candidates:
        name = cand.name
        model_type = cand.type
        param_grid = {f"clf__{k}": v for k,v in cand.params.items()} 
        scaler_needed = True 
        pipe = build_pipeline(model_type, {}, scaler=scaler_needed, random_state=cfg.data.random_state)
        if cfg.model.optimize:
            search = tune_model(pipe, param_grid, X_train, y_train, cv, cfg.model.scoring, method=cfg.model.optimization_method, n_iter=cfg.model.optimization_n_iter)
            model = search.best_estimator_
            score = search.best_score_
        else:
            scores = cross_validate_model(pipe, X_train, y_train, cfg.model.cv_n_splits, cfg.model.cv_shuffle, cfg.data.random_state, cfg.model.scoring)
            score = scores[f"test_{cfg.model.scoring[0]}"].mean()
            model = pipe.fit(X_train, y_train)
        
        logger.info(f"Candidato {name}: score CV {score:.3f}")

        if score > best_score:
            best_score = score
            best_model = model
            best_name = name

    logger.info(f"Melhor modelo: {best_name} com score {best_score:.3f}")

    model_dir = cfg.output.model_dir
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, f"best_model.joblib")
    joblib.dump(best_model, model_path)
    logger.info(f"Modelo salvo em {model_path}")
    report_dir = cfg.output.report_dir
    evaluate_model(best_model, X_test, y_test, class_names=['Kama','Rosa','Canadian'], output_dir=report_dir, prefix=f"test_{best_name}")
    logger.info("Processo de treino concluído")

if __name__ == "__main__":
    main()
