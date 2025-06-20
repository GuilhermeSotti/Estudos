import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import os
import joblib
import logging

logger = logging.getLogger(__name__)

def check_missing(df: pd.DataFrame) -> pd.Series:
    return df.isna().sum()

def handle_outliers(df: pd.DataFrame, columns: list[str], method: str = "iqr", factor: float = 1.5) -> pd.DataFrame:
    """
    Exemplo: remove ou marca outliers com base em IQR. Retorna DataFrame filtrado ou com NaNs.
    """
    df2 = df.copy()
    for col in columns:
        Q1 = df2[col].quantile(0.25)
        Q3 = df2[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - factor * IQR
        upper = Q3 + factor * IQR
        mask = df2[col].between(lower, upper)
        logger.debug(f"{col}: removendo {(~mask).sum()} outliers")
        df2 = df2[mask]
    return df2.reset_index(drop=True)

def split_data(df: pd.DataFrame, feature_cols: list[str], target_col: str, test_size: float,
               random_state: int, stratify: bool = True):
    X = df[feature_cols]
    y = df[target_col]
    if stratify:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, stratify=y, random_state=random_state)
    else:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state)
    logger.info(f"Split: {len(X_train)} treino, {len(X_test)} teste")
    return X_train, X_test, y_train, y_test

def fit_scaler(X_train: pd.DataFrame, scaler_type: str = "standard") -> StandardScaler | MinMaxScaler:
    if scaler_type == "standard":
        scaler = StandardScaler()
    else:
        scaler = MinMaxScaler()
    scaler.fit(X_train)
    logger.info(f"Scaler {scaler_type} ajustado em treino")
    return scaler

def save_scaler(scaler, output_dir: str, filename: str = "scaler.joblib"):
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, filename)
    joblib.dump(scaler, path)
    logger.info(f"Scaler salvo em {path}")
