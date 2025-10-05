import sqlite3
import json
import time
from paho.mqtt import client as mqtt_client
import requests

BROKER = 'broker.hivemq.com'
PORT = 1883
TOPIC = "farmtech/sensors"
API_URL = "http://localhost:5000/predict"
DB_PATH = "iot_data.db"

def on_connect(client, userdata, flags, rc):
    print("Conectado MQTT com rc:", rc)
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print("Recebido:", payload)
    try:
        data = json.loads(payload)
    except Exception as e:
        print("JSON inválido", e)
        return

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            payload TEXT
        )
    ''')
    c.execute("INSERT INTO readings (payload) VALUES (?)", (json.dumps(data),))
    conn.commit()
    conn.close()
    features = data
    try:
        r = requests.post(API_URL, json={"features": features}, timeout=5)
        print("API status:", r.status_code, r.text)
    except Exception as e:
        print("Erro ao chamar API:", e)

def run():
    client = mqtt_client.Client("bridge-client")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT)
    client.loop_forever()

if __name__ == "__main__":
    run()
