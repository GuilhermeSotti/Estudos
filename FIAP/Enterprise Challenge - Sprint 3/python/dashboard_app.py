import os
import json
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import pickle
from datetime import datetime

st.set_page_config(page_title="PM Dashboard", layout="wide")
st.title("Manutenção Preditiva — Demo")

DATA_SOURCE = st.sidebar.selectbox("Fonte de dados", ["CSV (simulado)", "PostgreSQL"])
if DATA_SOURCE == "CSV (simulado)":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path_default = os.path.join(base_dir, "..", "input", "simulated_readings.csv")
    csv_path_default = os.path.abspath(csv_path_default)
    csv_path = st.sidebar.text_input("Caminho CSV", csv_path_default)
    if not os.path.exists(csv_path):
        st.error("CSV não encontrado. Coloque simulated_readings.csv no diretório.")
        st.stop()
    df = pd.read_csv(csv_path, parse_dates=["timestamp"])
else:
    st.sidebar.info("Configurar conexão PostgreSQL")
    pg_host = st.sidebar.text_input("PG Host", "localhost")
    pg_port = st.sidebar.text_input("PG Port", "5432")
    pg_db = st.sidebar.text_input("PG DB", "pm_db")
    pg_user = st.sidebar.text_input("PG User", "postgres")
    pg_pass = st.sidebar.text_input("PG Pass", type="password")
    if st.sidebar.button("Carregar dados do Postgres"):
        from sqlalchemy import create_engine
        engine = create_engine(f"postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}")
        q = "SELECT r.ts as timestamp, s.type as sensor_type, r.value FROM reading r JOIN sensor s ON r.sensor_id = s.sensor_id ORDER BY r.ts LIMIT 5000;"
        raw = pd.read_sql(q, engine, parse_dates=["timestamp"])
        df = raw.pivot_table(index="timestamp", columns="sensor_type", values="value").reset_index()
        st.success("Dados carregados")
    else:
        st.stop()

st.sidebar.header("Parâmetros")
vib_th = st.sidebar.slider("Threshold Vibração (g)", 0.5, 5.0, 1.5)
temp_th = st.sidebar.slider("Threshold Temperatura (°C)", 30.0, 120.0, 60.0)
show_model = st.sidebar.checkbox("Carregar modelo ML (model_best.pkl)", value=False)
fft_window = st.sidebar.number_input("FFT window (samples)", min_value=8, max_value=1024, value=64, step=8)

st.subheader("Preview dos dados (head)")
st.dataframe(df.head())

st.subheader("Séries temporais")
fig, axs = plt.subplots(2, 1, figsize=(12, 4), sharex=True)
if "vibration" in df.columns:
    axs[0].plot(df["timestamp"], df["vibration"])
axs[0].set_ylabel("Vibração (g)")
if "temperature" in df.columns:
    axs[1].plot(df["timestamp"], df["temperature"])
axs[1].set_ylabel("Temperatura (°C)")
st.pyplot(fig)

st.subheader("Alertas simples por threshold")
alerts = df[
    (df.get("vibration", pd.Series(0, index=df.index)) > vib_th) |
    (df.get("temperature", pd.Series(0, index=df.index)) > temp_th)
]
st.write(f"Número de alertas nesta janela: {len(alerts)}")
st.dataframe(alerts.head(200))

def extract_fft_bands(signal, n_bands=4):
    """Retorna média de magnitude em n_bands para um sinal 1D (numpy)."""
    if len(signal) < 4:
        return [0.0] * n_bands
    spec = np.abs(np.fft.rfft(signal))
    L = len(spec)
    if L == 0:
        return [0.0] * n_bands
    bands = []
    for i in range(n_bands):
        start = int(i * (L / n_bands))
        end = int((i + 1) * (L / n_bands)) if i < n_bands - 1 else L
        seg = spec[start:end] if end > start else spec[start:start+1]
        bands.append(float(np.mean(seg)) if seg.size > 0 else 0.0)
    return bands

def build_features_for_inference(df_input, fft_window=64):
    """Constrói features identicamente ao pipeline de treino (rolling + FFT bands)."""
    df2 = df_input.copy()
    if "vibration" not in df2.columns:
        df2["vibration"] = 0.0
    if "temperature" not in df2.columns:
        df2["temperature"] = 0.0

    df2["vib_rm5"] = df2["vibration"].rolling(5, min_periods=1).mean()
    df2["vib_rstd5"] = df2["vibration"].rolling(5, min_periods=1).std().fillna(0)
    df2["temp_rm5"] = df2["temperature"].rolling(5, min_periods=1).mean()
    df2["temp_rstd5"] = df2["temperature"].rolling(5, min_periods=1).std().fillna(0)

    n = len(df2)
    fft_bands = np.zeros((n, 4))
    vib_vals = df2["vibration"].fillna(method="ffill").fillna(0).values
    for i in range(n):
        start = max(0, i - int(fft_window) + 1)
        seg = vib_vals[start:i+1]
        if len(seg) < 4:
            fft_bands[i, :] = 0.0
        else:
            fft_bands[i, :] = extract_fft_bands(seg, n_bands=4)
    for j in range(4):
        df2[f"fft_b{j+1}"] = fft_bands[:, j]

    return df2

if show_model:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    default_model_path = os.path.abspath(os.path.join(base_dir, "..", "output", "model_best.pkl"))
    model_path = st.sidebar.text_input("Modelo (pickle)", default_model_path)

    features_json_path = os.path.abspath(os.path.join(base_dir, "..", "output", "model_features.json"))

    if os.path.exists(model_path):
        with open(model_path, "rb") as f:
            model = pickle.load(f)
        st.success("Modelo carregado")

        df2 = build_features_for_inference(df, fft_window=int(fft_window))

        feature_names = None
        if os.path.exists(features_json_path):
            try:
                with open(features_json_path, "r") as fh:
                    feature_names = json.load(fh)
                # valida tipo
                if not isinstance(feature_names, list):
                    feature_names = None
            except Exception:
                feature_names = None

        if feature_names is None:
            try:
                feature_names = list(model.feature_names_in_)
            except Exception:
                feature_names = [
                    "vibration", "temperature",
                    "vib_rm5", "vib_rstd5", "temp_rm5", "temp_rstd5",
                    "fft_b1", "fft_b2", "fft_b3", "fft_b4"
                ]

        for col in feature_names:
            if col not in df2.columns:
                df2[col] = 0.0

        X = df2[feature_names].fillna(0)

        try:
            preds = model.predict(X)
        except ValueError as ve:
            missing = set(feature_names) - set(df2.columns)
            for c in missing:
                df2[c] = 0.0
            X = df2[feature_names].fillna(0)
            preds = model.predict(X)

        probs = None
        try:
            probs = model.predict_proba(X)[:, 1]
        except Exception:
            probs = None

        df2["pred_label"] = preds
        if probs is not None:
            df2["pred_prob"] = probs

        st.subheader("Resultados do modelo (head)")
        cols_to_show = ["timestamp", "vibration", "temperature", "pred_label"]
        if probs is not None:
            cols_to_show.append("pred_prob")
        if "timestamp" not in df2.columns:
            df2 = df2.reset_index().rename(columns={"index": "timestamp"})
        st.dataframe(df2[cols_to_show].head(200))
    else:
        st.warning("Modelo não encontrado no caminho especificado.")
