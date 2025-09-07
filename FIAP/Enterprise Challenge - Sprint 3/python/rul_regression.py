# Gera labels RUL (tempo até próxima falha) e treina um regressor (RandomForest).
#
# Uso:
# python rul_regression.py --csv simulated_readings.csv --out rul_model.pkl

import argparse
import json
import numpy as np
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

def compute_rul(df):
    """RUL = minutos até o início da próxima janela com label==1.
    Se não houver falha no futuro, retorna NaN."""
    n = len(df)
    idxs_fail = np.where(df["label"].values == 1)[0]
    rul = np.full(n, np.nan)
    if len(idxs_fail) == 0:
        return rul
    next_idx_ptr = 0
    for i in range(n):
        while next_idx_ptr < len(idxs_fail) and idxs_fail[next_idx_ptr] < i:
            next_idx_ptr += 1
        if next_idx_ptr >= len(idxs_fail):
            rul[i] = np.nan
        else:
            rul[i] = idxs_fail[next_idx_ptr] - i
    return rul

def build_features(df):
    df = df.copy()
    df["vib_rm5"] = df["vibration"].rolling(5, min_periods=1).mean()
    df["temp_rm5"] = df["temperature"].rolling(5, min_periods=1).mean()
    features = ["vibration", "temperature", "vib_rm5", "temp_rm5"]
    X = df[features].fillna(0)
    y = df["RUL"]
    return X, y, features

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--out", default="rul_model.pkl")
    args = ap.parse_args()
    df = pd.read_csv(args.csv, parse_dates=["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)
    df["RUL"] = compute_rul(df)
    train_df = df[~df["RUL"].isna()].copy()
    if train_df.empty:
        print("Nenhuma amostra com RUL finito — verifique labels.")
        return
    X, y, feats = build_features(train_df)
    split = int(0.7 * len(X))
    X_train, X_test = X.iloc[:split], X.iloc[split:]
    y_train, y_test = y.iloc[:split], y.iloc[split:]
    model = RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    with open(args.out, "wb") as f:
        pickle.dump(model, f)
    metrics = {"mse": float(mse), "r2": float(r2), "n_train": len(X_train), "n_test": len(X_test), "features": feats}
    with open("rul_metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)
    print("RUL treino concluído. MSE:", mse, "R2:", r2)

if __name__ == "__main__":
    main()