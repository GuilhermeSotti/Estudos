from .utils import load_config, get_logger, sql_connection, fetch_json
import pandas as pd

logger = get_logger(__name__)

def ingest_comexstat(product_code: str, year: int, flow: str = "Export"):
    """
    Coleta dados COMEXSTAT e grava raw em Oracle.
    :param product_code: NCM ou código do produto
    :param year: ano de interesse
    :param flow: 'Export' ou 'Import'
    """
    cfg = load_config()["comexstat"]
    url = f"{cfg['base_url']}/tables/product-categories"
    params = {"produto": product_code, "ano": year, "fluxo": flow.lower()}
    logger.info(f"Iniciando ingestão COMEXSTAT para {product_code} {year} {flow}")
    data = fetch_json(url, params=params, timeout=cfg["timeout"])
    df = pd.DataFrame(data["data"]["list"])
    conn = sql_connection()

    cursor = conn.cursor()
    sql = """
    INSERT INTO raw_data.tb_comexstat_raw
      (source, ingest_ts, payload)
    VALUES
        (?, GETDATE(), ?)
    """
    for _, row in df.iterrows():
        payload_json = row.to_json(date_format='iso')
        cursor.execute(sql, "COMEXSTAT", payload_json)

    conn.commit()
    cursor.close()
    conn.close()
    logger.info("Ingestão COMEXSTAT concluída.")

    return df