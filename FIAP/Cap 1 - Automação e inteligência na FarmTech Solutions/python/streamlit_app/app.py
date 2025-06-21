import streamlit as st
import pandas as pd
from ml.predict import predict_next
from streamlit_app.utils import fetch_recent_data, format_timestamp
from ml.train_model import train_and_export
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="FarmTech Dashboard", layout="wide")
st.title("FarmTech Solutions - Dashboard")

with st.sidebar:
    st.header("Controles")
    if st.button("Retrain Model"):
        with st.spinner("Treinando modelo..."):
            train_and_export()
        st.success("Modelo retrainado com sucesso!")

    threshold = st.slider("Threshold mínima de umidade (%)", min_value=0, max_value=100, value=30)
    st.markdown("Avisa se previsão de umidade ficar abaixo deste valor.")

st_autorefresh(interval=60000, key="datarefresh")

df = fetch_recent_data(limit=300)

st.subheader("Série Temporal de Umidade e Nutrientes")
if df.empty:
    st.warning("Sem dados para exibir.")
else:
    chart_data = df.set_index("timestamp")[["umidade", "nutriente"]]
    st.line_chart(chart_data)

st.subheader("Previsão de Umidade Futura")
if df.empty or len(df) < 2:
    st.warning("Dados insuficientes para previsão.")
else:
    try:
        next_umid = predict_next(df)
        st.metric("Umidade Prevista", f"{next_umid:.2f}%")
        if next_umid < threshold:
            st.warning(f"Previsão abaixo do threshold ({threshold}%). Considere irrigar.")
    except Exception as e:
        st.error(f"Erro ao prever: {e}")

st.subheader("Últimas Leituras")
if df.empty:
    st.info("Nenhuma leitura disponível.")
else:
    df_display = format_timestamp(df.reset_index(drop=True))
    st.dataframe(df_display)

st.markdown("---")
st.caption("Dados atualizados a cada 60 segundos (cache). Use o botão de retrain para refinar o modelo com dados novos.")