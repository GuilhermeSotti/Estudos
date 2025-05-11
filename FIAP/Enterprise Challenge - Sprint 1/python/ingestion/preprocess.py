import os
import json
import glob
import pandas as pd
from config.settings import S3_BUCKET, AWS_REGION
import boto3
import logging
from config.logging_config import setup_logging

setup_logging()
logger = logging.getLogger("preprocess")

def download_raw_files(local_dir="data/raw"):
    os.makedirs(local_dir, exist_ok=True)
    s3 = boto3.resource("s3", region_name=AWS_REGION)
    bucket = s3.Bucket(S3_BUCKET)
    for obj in bucket.objects.filter(Prefix="raw/"):
        dest = os.path.join(local_dir, os.path.basename(obj.key))
        bucket.download_file(obj.key, dest)
        logger.debug(f"Baixado {obj.key} → {dest}")
    return glob.glob(os.path.join(local_dir, "*.json"))

def transform_to_parquet(json_files, output_path="data/processed/sensor_data.parquet"):
    records = []
    for f in json_files:
        with open(f, "r") as fh:
            data = json.load(fh)
            # Normalização / enriquecimento se necessário
            records.append({
                "timestamp": pd.to_datetime(data["timestamp"], unit="s"),
                "temperature": data["temperature"],
                "vibration": data["vibration"]
            })
    df = pd.DataFrame(records)
    df.sort_values("timestamp", inplace=True)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_parquet(output_path, index=False)
    logger.info(f"Dados transformados em Parquet: {output_path}")
    return output_path

if __name__ == "__main__":
    files = download_raw_files()
    transform_to_parquet(files)
    logger.info("Processamento concluído")