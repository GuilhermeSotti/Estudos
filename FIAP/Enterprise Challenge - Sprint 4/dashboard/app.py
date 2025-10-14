import streamlit as st
import pandas as pd
import joblib
import psycopg2
from datetime import datetime
import time

st.set_page_config(page_title="Factory MVP Dashboard")

conn = psycopg2.connect(host="localhost", dbname="factorydb", user="postgres", password="postgres")
@st.cache(ttl=10)
def load_latest(n=200):
    return pd.read_sql("SELECT * FROM measurements ORDER BY ts DESC LIMIT %s", conn, params=(n,))

df = load_latest(500)
st.title("Factory — Dashboard MVP")
st.metric("Última temperatura (°C)", value=f"{df['temperature_c'].iloc[0]:.2f}")
st.metric("Média 1h", value=f"{df['temperature_c'].mean():.2f}")

st.subheader("Série temporal")
st.line_chart(df[['ts','temperature_c']].set_index('ts'))

model = joblib.load("../ml/models/rf_temp.joblib")
X = pd.DataFrame({
    'temp_lag1': df['temperature_c'].shift(1).fillna(method='bfill'),
    'humidity': df['humidity'],
    'hour': pd.to_datetime(df['ts']).dt.hour
})
pred = model.predict(X)
df['pred'] = pred
st.subheader("Previsão vs Real (últimos registros)")
st.line_chart(df.set_index('ts')[['temperature_c','pred']])

THRESH = st.sidebar.number_input("Threshold temperatura (°C)", value=70.0)
recent = df.iloc[0]
if recent['temperature_c'] > THRESH:
    st.error(f"ALERTA: temperatura {recent['temperature_c']:.2f}°C > {THRESH}°C — device {recent['device_id']}")

    cur = conn.cursor()
    cur.execute("INSERT INTO alerts(device_id, ts, alert_type, value, message) VALUES (%s,%s,%s,%s,%s)",
                (recent['device_id'], datetime.utcnow(), 'HIGH_TEMP', recent['temperature_c'], 'Threshold exceeded via dashboard'))
    conn.commit()
    cur.close()
else:
    st.success("Sem alertas críticos")

st.subheader("Contagem de alertas (últimas 24h)")
alerts_df = pd.read_sql("SELECT * FROM alerts WHERE ts > now() - interval '24 hours'", conn)
st.write(alerts_df)
