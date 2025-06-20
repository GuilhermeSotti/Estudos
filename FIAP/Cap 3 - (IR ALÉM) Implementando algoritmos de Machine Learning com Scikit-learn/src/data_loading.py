import pandas as pd
import os
import logging

logger = logging.getLogger(__name__)

def load_seeds_raw(raw_path: str) -> pd.DataFrame:
    """
    Lê o arquivo raw do Seeds Dataset e retorna DataFrame com colunas nomeadas,
    incluindo coluna 'class' (inteiro) e 'class_name' (string).
    """
    colnames = ['area','perimeter','compactness','length','width','asymmetry','groove','class']
    if not os.path.exists(raw_path):
        raise FileNotFoundError(f"Arquivo raw não encontrado em {raw_path}. Baixe e coloque em data/raw/")
    df = pd.read_csv(raw_path, sep='\s+', header=None, names=colnames)
    mapping = {1: 'Kama', 2: 'Rosa', 3: 'Canadian'}
    df['class_name'] = df['class'].map(mapping)
    logger.info(f"Seeds raw carregado com {len(df)} amostras")
    return df

def save_processed_df(df: pd.DataFrame, processed_dir: str, filename: str):
    os.makedirs(processed_dir, exist_ok=True)
    path = os.path.join(processed_dir, filename)
    df.to_csv(path, index=False)
    logger.info(f"DataFrame salvo em {path}")
