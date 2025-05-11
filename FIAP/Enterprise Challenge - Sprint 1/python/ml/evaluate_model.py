import os
import logging
import pandas as pd
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
from config.logging_config import setup_logging

setup_logging()
logger = logging.getLogger("evaluate_model")

def evaluate(model_path="models/rf_model.pkl", data_path="data/processed/sensor_data.parquet"):
    df = pd.read_parquet(data_path)
    X = df.drop(['timestamp'], axis=1).dropna()
    y_true = X.pop('target')
    model = joblib.load(model_path)
    y_pred = model.predict(X)
    mae = mean_absolute_error(y_true, y_pred)
    r2  = r2_score(y_true, y_pred)
    logger.info(f"MAE: {mae:.4f}, R2: {r2:.4f}")
    # Opcional: salvar relatório em CSV/JSON
    report = {
        "MAE": mae,
        "R2": r2
    }
    report_path = os.path.join("models", "evaluation_report.json")
    pd.Series(report).to_json(report_path, indent=4)
    logger.info(f"Relatório de avaliação salvo em {report_path}")
    return report_path

if __name__ == "__main__":
    evaluate()
