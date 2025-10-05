import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib

def load_data(path="../data/crop_yield.csv"):
    df = pd.read_csv(path)
    return df

def basic_cleaning(df):
    df = df.copy()
    df.columns = [c.strip().lower().replace(" ", "_").replace("(", "").replace(")", "") for c in df.columns]
    for col in ['precipitacao', 'umidade_especifica_a_2_m', 'umidade_relativa_a_2_m', 'temperatura_a_2_m', 'rendimento']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.drop_duplicates()
    df = df.fillna(df.median(numeric_only=True))
    return df

def feature_engineering(df):
    df = df.copy()
    if 'cultura' in df.columns:
        df = pd.get_dummies(df, columns=['cultura'], drop_first=True)
    return df

def prepare_train_test(df, target='rendimento', test_size=0.2, random_state=42):
    X = df.drop(columns=[target])
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                        test_size=test_size,
                                                        random_state=random_state)
    scaler = StandardScaler()
    numeric_cols = X_train.select_dtypes(include=np.number).columns.tolist()
    X_train[numeric_cols] = scaler.fit_transform(X_train[numeric_cols])
    X_test[numeric_cols] = scaler.transform(X_test[numeric_cols])
    joblib.dump(scaler, "../models/scaler.joblib")
    return X_train, X_test, y_train, y_test
