import json
import ssl
import paho.mqtt.client as mqtt
from config.settings import MQTT_BROKER, MQTT_PORT, MQTT_TOPIC
from config.logging_config import setup_logging
import logging

setup_logging()
logger = logging.getLogger("mqtt_publish")

def publish_data(payload: dict):
    client = mqtt.Client()
    client.tls_set(cert_reqs=ssl.CERT_REQUIRED)
    client.connect(MQTT_BROKER, MQTT_PORT)
    msg = json.dumps(payload)
    client.publish(MQTT_TOPIC, msg)
    logger.debug(f"Publicado no tópico {MQTT_TOPIC}: {msg}")
    client.disconnect()

if __name__ == "__main__":
    # Exemplo de uso
    sample = {"timestamp": 0, "temperature": 25.0, "vibration": 1.2}
    publish_data(sample)
    logger.info("Publicação de exemplo concluída")
