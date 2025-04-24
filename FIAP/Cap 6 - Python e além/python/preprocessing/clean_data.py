import pandas as pd

def drop_missing(df: pd.DataFrame, thresh: float = 0.8) -> pd.DataFrame:
    """
    Remove colunas com percentuais de dados faltantes acima do threshold.
    :param thresh: proporção mínima de não-nulos (entre 0 e 1)
    """
    min_count = int(thresh * len(df))
    return df.dropna(axis=1, thresh=min_count)

def fill_defaults(df: pd.DataFrame, defaults: dict) -> pd.DataFrame:
    """
    Preenche valores faltantes conforme dicionário {col: valor}.
    """
    return df.fillna(value=defaults)
