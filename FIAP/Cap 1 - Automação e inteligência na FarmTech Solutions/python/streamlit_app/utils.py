import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
from ml_pipeline.config import DB_URI

@st.cache_data(ttl=60)
def fetch_recent_data(limit: int = 200) -> pd.DataFrame:
    """
    Busca os últimos N registros do banco para exibir no dashboard.
    """
    engine = create_engine(DB_URI, echo=False, pool_pre_ping=True)
    df = pd.read_sql(
        "SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT :lim",
        engine,
        params={"lim": limit},
        parse_dates=["timestamp"]
    )
    return df.sort_values("timestamp")

def format_timestamp(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["timestamp"] = df["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")
    return df
