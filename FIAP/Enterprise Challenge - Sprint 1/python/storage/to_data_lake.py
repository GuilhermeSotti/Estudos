import os
import glob
import logging
import boto3
from config.settings import S3_BUCKET, AWS_REGION
from config.logging_config import setup_logging

setup_logging()
logger = logging.getLogger("to_data_lake")

def upload_processed_files(local_pattern="data/processed/*.parquet", s3_prefix="processed/"):
    s3 = boto3.client("s3", region_name=AWS_REGION)
    files = glob.glob(local_pattern)
    for path in files:
        key = os.path.join(s3_prefix, os.path.basename(path))
        s3.upload_file(path, S3_BUCKET, key)
        logger.info(f"Upload para Data Lake: s3://{S3_BUCKET}/{key}")

if __name__ == "__main__":
    upload_processed_files()
