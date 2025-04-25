import os
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

def train_yield_model(df: pd.DataFrame, features: list, target: str, out_path: str):
    """
    Treina RandomForestRegressor e salva o modelo em disco.
    """
   
    dirpath = os.path.dirname(out_path)
    if dirpath and not os.path.isdir(dirpath):
        os.makedirs(dirpath, exist_ok=True)

    X, y = df[features], df[target]
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    joblib.dump(model, out_path)
    return model


def predict_yield(model_path: str, X_new: pd.DataFrame) -> pd.Series:
    """
    Carrega modelo e retorna previsões.
    """
    model = joblib.load(model_path)
    return pd.Series(model.predict(X_new), index=X_new.index)
