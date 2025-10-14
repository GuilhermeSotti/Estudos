import json, time
import paho.mqtt.client as mqtt
import psycopg2
from datetime import datetime
import os

MQTT_TOPIC = "factory/sensor/+"
BROKER = os.getenv("MQTT_BROKER","localhost")

conn = psycopg2.connect(
    host=os.getenv("PG_HOST","localhost"),
    dbname=os.getenv("PG_DB","factorydb"),
    user=os.getenv("PG_USER","postgres"),
    password=os.getenv("PG_PASS","postgres")
)
conn.autocommit = True
cur = conn.cursor()

def upsert_device(device_id):
    cur.execute("""INSERT INTO devices(device_id) VALUES (%s) ON CONFLICT (device_id) DO NOTHING""",(device_id,))

def insert_measurement(device_id, ts, temp, hum):
    cur.execute("""
        INSERT INTO measurements(device_id, ts, temperature_c, humidity)
        VALUES (%s, %s, %s, %s)
    """, (device_id, ts, temp, hum))

def on_connect(client, userdata, flags, rc):
    print("Connected", rc)
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        device_id = payload.get("device_id","unknown")
        ts = datetime.utcnow()

        if isinstance(payload.get("ts"), (int,float)):
            maybe = int(payload.get("ts"))
            if maybe > 1e10:
                ts = datetime.utcfromtimestamp(maybe/1000.0)
        temp = float(payload.get("temp", None))
        hum = float(payload.get("hum", None))
        upsert_device(device_id)
        insert_measurement(device_id, ts, temp, hum)
        print("Inserted:", device_id, ts, temp, hum)
    except Exception as e:
        print("Error parsing message:", e)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, 1883, 60)
client.loop_forever()
