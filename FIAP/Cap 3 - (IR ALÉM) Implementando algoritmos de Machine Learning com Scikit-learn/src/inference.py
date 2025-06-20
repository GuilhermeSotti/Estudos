import joblib
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def load_model(model_path: str):
    model = joblib.load(model_path)
    logger.info(f"Modelo carregado de {model_path}")
    return model

def predict_instance(model, features: dict, feature_order: list[str]):
    """
    features: dict com chaves igual feature_order; retorna label previsto e, se disponível, probabilidade.
    """
    X = pd.DataFrame([features], columns=feature_order)
    pred = model.predict(X)[0]
    result = {"prediction": int(pred)}
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(X)[0]
        result["probabilities"] = proba.tolist()
    logger.info(f"Predição para instância: {result}")
    return result

def predict_batch(model, df: pd.DataFrame, feature_cols: list[str]) -> pd.DataFrame:
    preds = model.predict(df[feature_cols])
    df_out = df.copy()
    df_out["prediction"] = preds
    return df_out
