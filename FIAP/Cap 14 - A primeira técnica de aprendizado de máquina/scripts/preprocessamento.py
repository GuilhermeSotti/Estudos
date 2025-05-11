import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

def carregar_dados(caminho_csv):
    df = pd.read_csv(caminho_csv)
    return df

def tratar_dados(df):
    df = df.drop_duplicates()
    df = df.dropna()
    return df

def normalizar_dados(X):
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return X_scaled, scaler

def separar_variaveis(df, target_col='label'):
    X = df.drop(columns=[target_col])
    y = df[target_col]
    return X, y

def dividir_dados(X, y, test_size=0.3, random_state=42):
    return train_test_split(X, y, test_size=test_size, random_state=random_state)
