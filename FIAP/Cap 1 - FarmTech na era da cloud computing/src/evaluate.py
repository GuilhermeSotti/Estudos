# src/evaluate.py
import pandas as pd
import matplotlib.pyplot as plt
import joblib
import numpy as np

def load_metrics(path="../artifacts/metrics.csv"):
    return pd.read_csv(path)

def plot_metrics(df_metrics):
    df = df_metrics.sort_values("rmse")
    df.plot(kind='bar', x='model', y=['rmse', 'mae'])
    plt.title("Comparação de Métricas")
    plt.ylabel("Erro")
    plt.savefig("../artifacts/metrics_bar.png", bbox_inches='tight')

def feature_importances(model_path="../models/rf_model.joblib", X_sample_path=None):
    model = joblib.load(model_path)
    try:
        X = pd.read_csv(X_sample_path) if X_sample_path else None
    except Exception:
        X = None
    if hasattr(model, 'feature_importances_') and X is not None:
        importances = model.feature_importances_
        features = X.columns
        idx = np.argsort(importances)[::-1]
        plt.figure(figsize=(8,6))
        plt.barh(features[idx], importances[idx])
        plt.xlabel("Importância")
        plt.tight_layout()
        plt.savefig("../artifacts/feature_importances.png")
    else:
        print("Não foi possível calcular feature importances (faltam dados ou suporte no modelo).")

if __name__ == "__main__":
    m = load_metrics()
    print(m)
    plot_metrics(m)
