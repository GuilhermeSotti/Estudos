import argparse
import logging
import os
import pandas as pd
import joblib
from src.logger import setup_logging
from src.inference import predict_batch

def main():
    parser = argparse.ArgumentParser(description="Realiza predição em lote usando modelo salvo.")
    parser.add_argument("--model_path", type=str, required=False,
                        help="Caminho para modelo joblib (.joblib), idealmente pipeline completo",
                        default="Cap 3 - (IR ALÉM) Implementando algoritmos de Machine Learning com Scikit-learn/outputs/models/best_model.joblib")
    parser.add_argument("--input_csv", type=str, required=False,
                        help="Caminho para CSV de entrada com colunas de features originais",
                        default="Cap 3 - (IR ALÉM) Implementando algoritmos de Machine Learning com Scikit-learn/data/processed/processed_seeds.csv")
    parser.add_argument("--output_csv", type=str, required=False,
                        help="Caminho para salvar CSV de saída com predições. Se não informado, salva em 'predictions.csv'.",
                        default="Cap 3 - (IR ALÉM) Implementando algoritmos de Machine Learning com Scikit-learn/outputs/figures/predictions.csv")
    parser.add_argument("--log_dir", type=str, required=False,
                        help="Diretório para logs desta execução", default="outputs/logs")
    args = parser.parse_args()

    setup_logging(args.log_dir, "INFO")
    logger = logging.getLogger(__name__)
    logger.info("Iniciando predição em lote")

    if not os.path.exists(args.model_path):
        logger.error(f"Modelo não encontrado em {args.model_path}")
        return
    if not os.path.exists(args.input_csv):
        logger.error(f"CSV de entrada não encontrado em {args.input_csv}")
        return

    model = joblib.load(args.model_path)
    logger.info(f"Modelo carregado de {args.model_path}")

    df_in = pd.read_csv(args.input_csv)
    logger.info(f"Dados de entrada: {df_in.shape[0]} linhas, {df_in.shape[1]} colunas")

    if hasattr(model, "feature_names_in_"):
        expected = list(model.feature_names_in_)
    else:
        try:
            expected = list(model.named_steps.get('preproc').feature_names_in_)
        except Exception:
            logger.warning("Não foi possível obter feature_names_in_; removendo colunas 'class' e 'class_name' manualmente")
            expected = [c for c in df_in.columns if c not in ("class", "class_name")]
    missing = [c for c in expected if c not in df_in.columns]
    if missing:
        logger.error(f"Colunas esperadas ausentes no input: {missing}")
        logger.info("Verifique se o CSV contém todas as features necessárias ou implemente cálculo de colunas derivadas antes da predição.")
        return
    df_features = df_in[expected].copy()

    try:
        df_out = predict_batch(model, df_features, feature_cols=expected)
    except Exception as e:
        logger.error(f"Erro em predict_batch: {e}")
        return

    if "prediction" in df_out.columns:
        label_map = {1: "Kama", 2: "Rosa", 3: "Canadian"}
        df_out["class_name"] = df_out["prediction"].map(label_map)

    df_result = pd.concat([df_in.reset_index(drop=True), df_out[["prediction","class_name"]]], axis=1)
    df_result.to_csv(args.output_csv, index=False)
    logger.info(f"Predições salvas em {args.output_csv}")

if __name__ == "__main__":
    main()