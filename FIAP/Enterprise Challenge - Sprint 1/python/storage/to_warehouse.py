import os
import logging
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from config.settings import REDSHIFT_HOST, AWS_REGION
from config.settings import S3_BUCKET  # assumindo dados no S3 também
from config.logging_config import setup_logging

# Parâmetros de conexão; no caso real, use IAM roles ou secrets manager
REDSHIFT_DB   = os.getenv("REDSHIFT_DB", "dev")
REDSHIFT_USER = os.getenv("REDSHIFT_USER", "awsuser")
REDSHIFT_PWD  = os.getenv("REDSHIFT_PWD", "")
REDSHIFT_PORT = int(os.getenv("REDSHIFT_PORT", 5439))

setup_logging()
logger = logging.getLogger("to_warehouse")

def copy_from_s3_to_redshift(table_name="sensor_features", 
                            s3_key="processed/sensor_data.parquet",
                            iam_role="arn:aws:iam::123456789012:role/RedshiftCopyRole"):
    """
    Utiliza comando COPY nativo do Redshift para ingestão em massa.
    """
    conn = psycopg2.connect(
        host=REDSHIFT_HOST,
        port=REDSHIFT_PORT,
        dbname=REDSHIFT_DB,
        user=REDSHIFT_USER,
        password=REDSHIFT_PWD
    )
    cursor = conn.cursor()
    copy_sql = f"""
        COPY {table_name}
        FROM 's3://{S3_BUCKET}/{s3_key}'
        IAM_ROLE '{iam_role}'
        FORMAT AS PARQUET;
    """
    cursor.execute(copy_sql)
    conn.commit()
    cursor.close()
    conn.close()
    logger.info(f"Tabela {table_name} atualizada via COPY de s3://{S3_BUCKET}/{s3_key}")

if __name__ == "__main__":
    copy_from_s3_to_redshift()
