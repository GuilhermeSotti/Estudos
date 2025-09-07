# Script para treinar modelos mais robustos (RandomForest, LightGBM quando disponível),
# extrair features (rolling stats + FFT bands), tratar desbalanceamento (SMOTE quando disponível).
#
# Uso:
# python ml_improvements.py --csv simulated_readings.csv --out model_best.pkl
#
# Dependências:
# pandas, numpy, scikit-learn, imbalanced-learn (opcional), lightgbm (opcional), matplotlib

import os
import argparse
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, f1_score, roc_auc_score

try:
    from imblearn.over_sampling import SMOTE
    HAS_SMOTE = True
except Exception:
    HAS_SMOTE = False

try:
    import lightgbm as lgb
    HAS_LGB = True
except Exception:
    HAS_LGB = False

def extract_fft_bands(signal, n_bands=4):
    """Recebe vetor 1D e devolve média de magnitude em bandas (n_bands)."""
    spec = np.abs(np.fft.rfft(signal))
    L = len(spec)
    bands = []
    for i in range(n_bands):
        start = i * (L // n_bands)
        end = (i + 1) * (L // n_bands) if i < n_bands - 1 else L
        bands.append(spec[start:end].mean() if end > start else 0.0)
    return bands

def add_features(df):
    df = df.copy()
    df["vib_rm5"] = df["vibration"].rolling(5, min_periods=1).mean()
    df["vib_rstd5"] = df["vibration"].rolling(5, min_periods=1).std().fillna(0)
    df["temp_rm5"] = df["temperature"].rolling(5, min_periods=1).mean()
    df["temp_rstd5"] = df["temperature"].rolling(5, min_periods=1).std().fillna(0)

    n = len(df)
    fft_bands = np.zeros((n, 4))
    window = 64
    vib_vals = df["vibration"].values
    for i in range(n):
        start = max(0, i - window + 1)
        seg = vib_vals[start:i+1]
        if len(seg) < 4:
            fft_bands[i, :] = 0.0
        else:
            bands = extract_fft_bands(seg, n_bands=4)
            fft_bands[i, :] = bands
    for j in range(4):
        df[f"fft_b{j+1}"] = fft_bands[:, j]
    return df

def train_models(X_train, y_train, X_test, y_test, out_model_path):
    models = {}
    rf = RandomForestClassifier(n_estimators=200, class_weight="balanced", random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)
    models["random_forest"] = rf

    if HAS_LGB:
        lgbm = lgb.LGBMClassifier(n_estimators=200, class_weight="balanced", random_state=42)
        lgbm.fit(X_train, y_train)
        models["lightgbm"] = lgbm

    best_name, best_score = None, -1
    reports = {}
    for name, model in models.items():
        y_pred = model.predict(X_test)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        cm = confusion_matrix(y_test, y_pred).tolist()
        rep = classification_report(y_test, y_pred, output_dict=True)
        reports[name] = {"f1": f1, "confusion_matrix": cm, "classification_report": rep}
        if f1 > best_score:
            best_score = f1
            best_name = name

    best_model = models[best_name]
    with open(out_model_path, "wb") as f:
        pickle.dump(best_model, f)
    return best_name, best_score, reports

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--out", default="model_best.pkl")
    args = ap.parse_args()
    df = pd.read_csv(args.csv, parse_dates=["timestamp"])
    df = add_features(df)
    feature_cols = ["vibration","temperature","vib_rm5","vib_rstd5","temp_rm5","temp_rstd5","fft_b1","fft_b2","fft_b3","fft_b4"]
    X = df[feature_cols].fillna(0)
    y = df["label"].astype(int)

    split_idx = int(0.7 * len(df))
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
    if HAS_SMOTE:
        sm = SMOTE(random_state=42)
        X_train_res, y_train_res = sm.fit_resample(X_train, y_train)
    else:
        from sklearn.utils import resample
        train_df = X_train.copy()
        train_df["label"] = y_train.values
        majority = train_df[train_df["label"] == 0]
        minority = train_df[train_df["label"] == 1]
        if len(minority) == 0:
            X_train_res, y_train_res = X_train, y_train
        else:
            minority_upsampled = resample(minority, replace=True, n_samples=len(majority), random_state=42)
            up = pd.concat([majority, minority_upsampled])
            y_train_res = up["label"]
            X_train_res = up.drop(columns=["label"])
    best_name, best_score, reports = train_models(X_train_res, y_train_res, X_test, y_test, args.out)

    metrics = {"best": best_name, "best_score": best_score, "reports": reports}
    output_dir = os.path.join(os.path.dirname(__file__), "..", "output")
    os.makedirs(output_dir, exist_ok=True)
    metrics_path = os.path.join(output_dir, "ml_metrics.json")
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=2)
    print("Treino concluído. Best:", best_name, "F1:", best_score)

if __name__ == "__main__":
    main()