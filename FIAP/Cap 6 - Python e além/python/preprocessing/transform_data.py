import pandas as pd

def normalize_numeric(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    """
    Aplica Min-Max scaling para as colunas numéricas listadas,
    ignorando colunas inexistentes e avisando quais não foram encontradas.
    """
    valid_cols = [c for c in cols if c in df.columns]

    if not valid_cols:
        print("Nenhuma coluna válida para normalização. Pulando etapa.")
        return df

    df_norm = df.copy()
    for col in valid_cols:
        min_val, max_val = df_norm[col].min(), df_norm[col].max()
        if pd.api.types.is_numeric_dtype(df_norm[col]):
            df_norm[col] = (df_norm[col] - min_val) / (max_val - min_val)
        else:
            print("Coluna '{col}' não será normalizada.")
    return df_norm

def encode_categorical(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    """
    Aplica one-hot encoding para as colunas categóricas.
    """
    return pd.get_dummies(df, columns=cols, drop_first=True)
