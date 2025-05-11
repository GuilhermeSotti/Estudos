import os
import json
import ssl
import boto3
import logging
from paho.mqtt.client import Client
from config.settings import (
    MQTT_BROKER, MQTT_PORT, MQTT_TOPIC,
    AWS_REGION, S3_BUCKET
)
from config.logging_config import setup_logging

setup_logging()
logger = logging.getLogger("mqtt_consumer")

# Inicializa cliente S3
s3 = boto3.client("s3", region_name=AWS_REGION)

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload)
        # Validações básicas
        if "temperature" in data and "vibration" in data:
            key = f"raw/{int(data['timestamp'])}.json"
            s3.put_object(Bucket=S3_BUCKET, Key=key, Body=msg.payload)
            logger.info(f"Persistido em S3: s3://{S3_BUCKET}/{key}")
        else:
            logger.warning(f"Payload inválido: {msg.payload}")
    except Exception as e:
        logger.error(f"Erro ao processar mensagem: {e}")

def main():
    client = Client()
    client.tls_set(cert_reqs=ssl.CERT_REQUIRED)
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT)
    client.subscribe(MQTT_TOPIC)
    logger.info(f"Inscrito em {MQTT_TOPIC}, aguardando mensagens...")
    client.loop_forever()

if __name__ == "__main__":
    main()
