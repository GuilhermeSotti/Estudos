import streamlit as st
from ml_pipeline.predict import predict_next
from streamlit_app.utils import fetch_recent_data, format_timestamp
from ml_pipeline.train_model import train_and_export

st.set_page_config(page_title="FarmTech Dashboard", layout="wide")
st.title("FarmTech Solutions")

with st.sidebar:
    st.header("Controles")
    if st.button("Retrain Model"):
        with st.spinner("Treinando modelo..."):
            train_and_export()
        st.success("Modelo retrainado com sucesso!")

df = fetch_recent_data(limit=300)

st.subheader("Série Temporal de Umidade e Nutrientes")
chart_data = df.set_index("timestamp")[["umidade", "nutriente"]]
st.line_chart(chart_data)

st.subheader("Previsão de Umidade Futura")
try:
    next_umid = predict_next(df)
    st.metric("Umidade Prevista", f"{next_umid:.2f}%")
except Exception as e:
    st.error(f"Erro ao prever: {e}")

st.subheader("Últimas Leituras")
st.dataframe(format_timestamp(df.reset_index(drop=True)))

st.markdown("---")
st.caption("Dados atualizados a cada 60 segundos. Use o botão de retrain para refinar o modelo com dados novos.")
