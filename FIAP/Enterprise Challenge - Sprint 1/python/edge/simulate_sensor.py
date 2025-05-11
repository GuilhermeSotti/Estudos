import time
import json
import random
import ssl
import paho.mqtt.client as mqtt
from config.settings import MQTT_BROKER, MQTT_PORT, MQTT_TOPIC
from config.logging_config import setup_logging
import logging

setup_logging()
logger = logging.getLogger("simulate_sensor")

def generate_payload():
    return {
        "timestamp": time.time(),
        "temperature": round(random.uniform(20.0, 80.0), 2),
        "vibration": round(random.uniform(0.0, 5.0), 3)
    }

def main():
    client = mqtt.Client()
    client.tls_set(cert_reqs=ssl.CERT_REQUIRED)
    client.connect(MQTT_BROKER, MQTT_PORT)
    logger.info(f"Conectado ao broker {MQTT_BROKER}:{MQTT_PORT}")

    try:
        while True:
            payload = generate_payload()
            msg = json.dumps(payload)
            client.publish(MQTT_TOPIC, msg)
            logger.debug(f"Enviado: {msg}")
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Simulação interrompida pelo usuário")
    finally:
        client.disconnect()

if __name__ == "__main__":
    main()
