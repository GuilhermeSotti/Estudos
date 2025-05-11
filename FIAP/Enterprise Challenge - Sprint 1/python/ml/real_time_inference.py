import os
import json
import logging
import joblib
from config.settings import TSDB_ENDPOINT
from influxdb import InfluxDBClient
from config.logging_config import setup_logging

setup_logging()
logger = logging.getLogger("real_time_inference")

# Carrega modelo uma vez (arquivo local ou via volume)
MODEL_PATH = os.getenv("MODEL_PATH", "/opt/models/rf_model.pkl")
model = joblib.load(MODEL_PATH)

def handler(event, context):
    """
    AWS Lambda / Azure Function handler.
    'event' contém o payload com os dados de entrada.
    """
    try:
        data = event.get("data") or json.loads(event.get("body", "{}"))
        features = [data[k] for k in ("temperature", "vibration", "temp_diff", "vib_roll_mean")]
        pred = model.predict([features])[0]
        logger.debug(f"Inferência: input={features} → pred={pred}")

        # Opcional: gravar resultado no TSDB
        influx = InfluxDBClient.from_dsn(TSDB_ENDPOINT)
        point = {
            "measurement": "predictions",
            "time": data.get("timestamp"),
            "fields": {"pred_temperature": float(pred)}
        }
        influx.switch_database("industrial_ts")
        influx.write_points([point])
        return {
            "statusCode": 200,
            "body": json.dumps({"prediction": pred})
        }
    except Exception as e:
        logger.error(f"Erro na inferência: {e}")
        return {"statusCode": 500, "body": str(e)}
