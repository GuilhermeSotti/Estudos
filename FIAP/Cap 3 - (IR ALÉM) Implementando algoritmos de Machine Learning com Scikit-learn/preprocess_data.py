import argparse
import logging
import os
from src.config import load_config
from src.logger import setup_logging
from src.data_loading import load_seeds_raw, save_processed_df
from src.preprocessing import check_missing, handle_outliers
from src.feature_engineering import calc_compactness, calc_ratio_length_width

def main():
    parser = argparse.ArgumentParser(description="Pré-processa o Seeds Dataset: carrega raw, trata missing/outliers, cria features e salva processed.")
    parser.add_argument("--config", type=str, required=False,
                        default="Cap 3 - (IR ALÉM) Implementando algoritmos de Machine Learning com Scikit-learn\config\default.yaml",
                        help="Caminho para arquivo YAML de configuração")
    parser.add_argument("--output_filename", type=str, default="processed_seeds.csv",
                        help="Nome do arquivo CSV de saída em processed_dir")
    args = parser.parse_args()

    cfg = load_config(args.config)
    setup_logging(cfg.output.log_dir, cfg.logging.get("level", "INFO"))
    logger = logging.getLogger(__name__)
    logger.info("Iniciando pré-processamento dos dados")

    df = load_seeds_raw(cfg.data.raw_path)

    miss = check_missing(df)
    logger.info(f"Missing por coluna:\n{miss.to_dict()}")

    if hasattr(cfg, "preprocessing") and getattr(cfg.preprocessing, "outlier_strategy", None):
        strat = cfg.preprocessing.outlier_strategy.lower()
    else:
        strat = "remove"
    cols = ['area','perimeter','length','width','asymmetry','groove']
    if strat == "remove":
        df = handle_outliers(df, columns=cols,
                             method=getattr(cfg.preprocessing, "outlier_method", "iqr"),
                             factor=getattr(cfg.preprocessing, "outlier_iqr_factor", 1.5))
        logger.info(f"Após remoção de outliers: {len(df)} amostras restantes")
    elif strat == "cap":
        from src.preprocessing import cap_outliers
        df = cap_outliers(df, columns=cols,
                          factor=getattr(cfg.preprocessing, "outlier_iqr_factor", 1.5))
        logger.info("Outliers capados para limites IQR")
    elif strat == "mark":
        from src.preprocessing import mark_outliers_iforest
        cont = getattr(cfg.preprocessing, "outlier_contamination", 0.05)
        df = mark_outliers_iforest(df, feature_cols=cols, cont=cont)
        logger.info("Outliers marcados com coluna 'is_outlier'")
    else:
        logger.warning(f"Estratégia de outlier desconhecida '{strat}'; pulando tratamento")


    if cfg.features.use_compactness:
        df = calc_compactness(df, area_col='area', perim_col='perimeter', out_col='compactness_calc')
    if cfg.features.use_ratio_length_width:
        df = calc_ratio_length_width(df, length_col='length', width_col='width', out_col='ratio_length_width')

    processed_dir = cfg.data.processed_dir
    os.makedirs(processed_dir, exist_ok=True)
    output_path = os.path.join(processed_dir, args.output_filename)
    save_processed_df(df, processed_dir, args.output_filename)
    logger.info(f"Pré-processamento concluído, DataFrame salvo em {output_path}")

if __name__ == "__main__":
    main()