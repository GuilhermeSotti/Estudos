import argparse
import logging
import os
import pandas as pd
import joblib
from src.config import load_config
from src.logger import setup_logging
from src.evaluation import evaluate_model
from src.preprocessing import split_data
from src.feature_engineering import calc_compactness, calc_ratio_length_width

def main():
    parser = argparse.ArgumentParser(description="Avalia um modelo salvo em dados processed.")
    parser.add_argument("--config", type=str, required=False, default="Cap 3 - (IR ALÉM) Implementando algoritmos de Machine Learning com Scikit-learn\config\default.yaml",
                        help="Caminho para arquivo YAML de configuração")
    parser.add_argument("--model_path", type=str, required=False,
                        help="Caminho para modelo joblib (.joblib). Se não informado, usa último em cfg.output.model_dir",
                        default="Cap 3 - (IR ALÉM) Implementando algoritmos de Machine Learning com Scikit-learn/outputs/models/best_model.joblib")
    parser.add_argument("--processed_path", type=str, required=False,
                        help="Caminho para CSV processed; se não informado, usa cfg.data.processed_dir/processed_seeds.csv",
                        default="Cap 3 - (IR ALÉM) Implementando algoritmos de Machine Learning com Scikit-learn/data/processed/processed_seeds.csv")
    args = parser.parse_args()

    cfg = load_config(args.config)
    setup_logging(cfg.output.log_dir, cfg.logging.get("level", "INFO"))
    logger = logging.getLogger(__name__)
    logger.info("Iniciando avaliação de modelo")

    if args.processed_path:
        processed_path = args.processed_path
    else:
        processed_path = os.path.join(cfg.data.processed_dir, "processed_seeds.csv")
    if not os.path.exists(processed_path):
        logger.error(f"Arquivo processed não encontrado: {processed_path}")
        return

    df = pd.read_csv(processed_path)
    if 'class' not in df.columns:
        logger.error("Coluna 'class' não encontrada em processed data")
        return

    feature_cols = ['area','perimeter']
    if cfg.features.use_compactness:
        if 'compactness_calc' not in df.columns:
            df = calc_compactness(df, area_col='area', perim_col='perimeter', out_col='compactness_calc')
        feature_cols.append('compactness_calc')
    if cfg.features.use_ratio_length_width:
        if 'ratio_length_width' not in df.columns:
            df = calc_ratio_length_width(df, length_col='length', width_col='width', out_col='ratio_length_width')
        feature_cols.append('ratio_length_width')
    for col in ['length','width','asymmetry','groove']:
        feature_cols.append(col)

    X_train, X_test, y_train, y_test = split_data(df, feature_cols, 'class',
                                                 cfg.data.test_size, cfg.data.random_state,
                                                 stratify=cfg.data.stratify)

    if args.model_path:
        model_path = args.model_path
    else:
        model_dir = cfg.output.model_dir
        if not os.path.isdir(model_dir):
            logger.error(f"Diretório de modelos não existe: {model_dir}")
            return
        candidates = sorted([f for f in os.listdir(model_dir) if f.endswith(".joblib")])
        if not candidates:
            logger.error(f"Nenhum modelo .joblib em {model_dir}")
            return
        model_path = os.path.join(model_dir, candidates[-1])
    if not os.path.exists(model_path):
        logger.error(f"Modelo não encontrado em {model_path}")
        return

    model = joblib.load(model_path)
    logger.info(f"Modelo carregado de {model_path}")

    try:
        report, metrics_summary, cm_path = evaluate_model(model, X_test, y_test,
                                                          class_names=['Kama','Rosa','Canadian'],
                                                          output_dir=cfg.output.report_dir,
                                                          prefix="eval")
        logger.info(f"Avaliação concluída. Métricas: {metrics_summary}")
        logger.info(f"Matriz de confusão salva em {cm_path}")
    except ValueError as e:
        logger.error(f"Erro ao predizer: {e}")
        if hasattr(model, "feature_names_in_"):
            expected = list(model.feature_names_in_)
            logger.error(f"Colunas esperadas pelo modelo: {expected}")
        logger.error(f"Colunas em X_test: {list(X_test.columns)}")
        return

if __name__ == "__main__":
    main()