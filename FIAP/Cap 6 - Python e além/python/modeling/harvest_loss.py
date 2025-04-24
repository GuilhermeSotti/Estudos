import pandas as pd
from sklearn.linear_model import LogisticRegression
import joblib

def train_harvest_loss(df: pd.DataFrame, features: list, target: str, out_path: str):
    """
    Treina modelo de classificação para risco de alta perda na colheita.
    """
    X, y = df[features], df[target]
    clf = LogisticRegression(max_iter=200)
    clf.fit(X, y)
    joblib.dump(clf, out_path)
    return clf

def predict_harvest_loss(model_path: str, X_new: pd.DataFrame) -> pd.Series:
    """
    Retorna probabilidade de perda elevada.
    """
    clf = joblib.load(model_path)
    return pd.Series(clf.predict_proba(X_new)[:,1], index=X_new.index)
