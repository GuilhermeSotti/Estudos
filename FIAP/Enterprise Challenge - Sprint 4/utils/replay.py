import time, json
import paho.mqtt.client as mqtt
import random
client = mqtt.Client()
client.connect("localhost",1883,60)
topic="factory/sensor/esp01"
for i in range(1000):
    payload = {"device_id":"esp01","ts":int(time.time()*1000),"temp":30+random.random()*20,"hum":40+random.random()*20}
    client.publish(topic, json.dumps(payload))
    print("Sent", payload)
    time.sleep(2)
