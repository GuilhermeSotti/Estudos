from joblib import load
import pandas as pd
from config import MODEL_PATH
from preprocessing import engineer_features, get_feature_target

_model = None

def _load_model():
    global _model
    if _model is None:
        _model = load(MODEL_PATH)
    return _model

def predict_next(df: pd.DataFrame) -> float:
    """
    Recebe DataFrame com registros recentes, prepara features
    e retorna a previsão da próxima umidade.
    """
    df_feat = engineer_features(df.tail(10))
    X, _ = get_feature_target(df_feat)
    model = _load_model()
    preds = model.predict(X)
    return float(preds[-1])
