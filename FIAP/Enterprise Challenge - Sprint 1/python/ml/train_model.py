import os
import logging
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib
from config.logging_config import setup_logging

setup_logging()
logger = logging.getLogger("train_model")

def load_features(path="data/processed/sensor_data.parquet"):
    df = pd.read_parquet(path)
    # Exemplo: criar features de janela, estatísticas, label
    df['temp_diff'] = df['temperature'].diff().fillna(0)
    df['vib_roll_mean'] = df['vibration'].rolling(window=5).mean().fillna(method='bfill')
    # Definir target (exemplo): próxima temperatura
    df['target'] = df['temperature'].shift(-1).fillna(df['temperature'])
    return df.dropna()

def train_and_save(model_path="models/rf_model.pkl"):
    df = load_features()
    X = df.drop(['timestamp', 'target'], axis=1)
    y = df['target']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    mse = mean_squared_error(y_test, preds)
    logger.info(f"Treino concluído. MSE no teste: {mse:.4f}")
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model, model_path)
    logger.info(f"Modelo salvo em {model_path}")
    return model_path, mse

if __name__ == "__main__":
    train_and_save()
