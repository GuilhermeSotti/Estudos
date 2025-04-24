from faostat import list_datasets_df, get_data
from .utils import get_logger, sql_connection
import pandas as pd

logger = get_logger(__name__)

def ingest_faostat(dataset_code: str, year: int):
    """
    Coleta dados FAOSTAT usando a biblioteca 'faostat' e grava raw em Oracle.

    :param dataset_code: código do dataset FAOSTAT (ex: 'QCL')
    :param year: ano de interesse (ex: 2022)
    :return: pandas.DataFrame com os dados coletados
    """
    logger.info(f"Iniciando ingestão FAOSTAT para {dataset_code}, ano {year}")

    data_list = get_data(
        code=dataset_code,
        pars={'year': year},
        show_flags=False,
        null_values=False,
        show_notes=False,
        strval=True
    )

    df = pd.DataFrame(data_list[1:], columns=data_list[0])
    logger.info(f"Dados FAOSTAT carregados em DataFrame com {len(df)} linhas")

    conn = sql_connection()
    cursor = conn.cursor()
    sql = """
    INSERT INTO raw_data.tb_faostat_raw
      (source, ingest_ts, payload)
    VALUES
        (?, GETDATE(), ?)
    """

    for _, row in df.iterrows():
        payload_json = row.to_json(date_format='iso')
        cursor.execute(sql, "FAOSTAT_LIB", payload_json)

    conn.commit()
    cursor.close()
    conn.close()

    logger.info("Ingestão FAOSTAT concluída.")

    return df