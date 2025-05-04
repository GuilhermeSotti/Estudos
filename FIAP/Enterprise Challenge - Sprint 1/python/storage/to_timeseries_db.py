import os
import logging
import pandas as pd
from influxdb import InfluxDBClient
from config.settings import TSDB_ENDPOINT
from config.logging_config import setup_logging

setup_logging()
logger = logging.getLogger("to_timeseries_db")

def load_parquet_to_timeseries(parquet_path="data/processed/sensor_data.parquet", 
                               dbname="industrial_ts", 
                               measurement="sensor_readings"):
    # lê arquivo Parquet
    df = pd.read_parquet(parquet_path)
    # formata para InfluxDB line protocol JSON
    points = []
    for _, row in df.iterrows():
        points.append({
            "measurement": measurement,
            "time": row["timestamp"].isoformat(),
            "fields": {
                "temperature": float(row["temperature"]),
                "vibration": float(row["vibration"])
            }
        })
    # conecta no TSDB
    client = InfluxDBClient.from_dsn(TSDB_ENDPOINT)
    client.create_database(dbname)
    client.switch_database(dbname)
    client.write_points(points, time_precision="ms", batch_size=1000)
    logger.info(f"{len(points)} pontos inseridos em {dbname}.{measurement}")

if __name__ == "__main__":
    load_parquet_to_timeseries()
