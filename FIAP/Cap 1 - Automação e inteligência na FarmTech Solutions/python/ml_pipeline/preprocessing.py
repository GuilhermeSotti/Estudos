import pandas as pd
from sqlalchemy import create_engine
from ml_pipeline.config import DB_URI

def load_data(table_name: str = "sensor_data", limit: int = None) -> pd.DataFrame:
    """
    Carrega dados brutos do banco de dados em um DataFrame.
    Se limit for fornecido, busca apenas os últimos N registros.
    """
    engine = create_engine(DB_URI, echo=False, pool_pre_ping=True)
    query = f"SELECT * FROM {table_name} ORDER BY timestamp"
    if limit:
        query += f" DESC LIMIT {limit}"
    df = pd.read_sql(query, engine, parse_dates=["timestamp"])
    return df

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Gera features a partir de timestamp e medidas brutas.
    Por exemplo: hora do dia, dia da semana, médias móveis.
    """
    df = df.copy()
    df["hour"] = df["timestamp"].dt.hour
    df["dayofweek"] = df["timestamp"].dt.dayofweek
    # Exemplo de média móvel de umidade (janela de 3 leituras)
    df["umidade_ma3"] = df["umidade"].rolling(3, min_periods=1).mean()
    # Target: umidade daqui a 1 leitura (ajuste conforme intervalo de coleta)
    df["umidade_futura"] = df["umidade"].shift(-1)
    df = df.dropna(subset=["umidade_futura"])
    return df

def get_feature_target(df: pd.DataFrame):
    """
    Separa features (X) e target (y) para treino.
    """
    features = ["umidade", "nutriente", "hour", "dayofweek", "umidade_ma3"]
    X = df[features]
    y = df["umidade_futura"]
    return X, y
