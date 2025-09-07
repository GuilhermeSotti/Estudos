#include <Arduino.h>
#include <WiFi.h>
#include <WiFiUdp.h>
#include <NTPClient.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include "esp32_config.h"
#include "vibration_sensor.h"
#include "temp_sensor.h"

#ifndef PIN_DS18B20
#define PIN_DS18B20 15
#endif

VibrationSensor vib;
TempSensor tempSensor(PIN_DS18B20);

WiFiClient espClient;
PubSubClient mqttClient(espClient);
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, NTP_POOL, NTP_OFFSET_SECS);

unsigned long lastPublish = 0;
const unsigned long publishInterval = PUBLISH_INTERVAL_MS;

String iso8601_now() {
  time_t raw = timeClient.getEpochTime();
  struct tm * ti = gmtime(&raw);
  char buf[32];
  strftime(buf, sizeof(buf), "%Y-%m-%dT%H:%M:%SZ", ti);
  return String(buf);
}

void connectWiFi() {
  if (WiFi.status() == WL_CONNECTED) return;
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  unsigned long start = millis();
  while (WiFi.status() != WL_CONNECTED) {
    delay(250);
    Serial.print(".");
    if (millis() - start > 20000) {
      Serial.println("\nWiFi timeout");
      break;
    }
  }
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWiFi conectado: " + WiFi.localIP().toString());
  }
}

void connectMQTT() {
  if (mqttClient.connected()) return;
  mqttClient.setServer(MQTT_BROKER, MQTT_PORT);
  String clientId = "ESP32-" + String((uint32_t)ESP.getEfuseMac(), HEX);
  int tries = 0;
  while (!mqttClient.connected() && tries < 6) {
    if (mqttClient.connect(clientId.c_str())) {
      Serial.println("MQTT conectado");
      break;
    } else {
      Serial.printf("MQTT falha (rc=%d). Tentando...\n", mqttClient.state());
      delay(2000);
      tries++;
    }
  }
}

void publish_readings() {
  float vib_g = vib.read_vibration_g();
  float temp_c = tempSensor.read_temperature_c();

  StaticJsonDocument<256> doc;
  doc["machine_id"] = MACHINE_ID;
  doc["timestamp"] = iso8601_now();

  JsonArray arr = doc.createNestedArray("sensors");
  JsonObject s1 = arr.createNestedObject();
  s1["type"] = "vibration";
  if (!isnan(vib_g)) { s1["value"] = vib_g; s1["unit"] = "g"; } else { s1["value"] = nullptr; }

  JsonObject s2 = arr.createNestedObject();
  s2["type"] = "temperature";
  if (!isnan(temp_c)) { s2["value"] = temp_c; s2["unit"] = "C"; } else { s2["value"] = nullptr; }

  char payload[512];
  serializeJson(doc, payload, sizeof(payload));

  String topic = String(MQTT_TOPIC_BASE) + "/" + String(MACHINE_ID) + "/sensors";
  if (!mqttClient.connected()) connectMQTT();
  bool ok = mqttClient.publish(topic.c_str(), payload);
  Serial.printf("publish ok=%d topic=%s payload=%s\n", ok, topic.c_str(), payload);
}

void setup() {
  Serial.begin(SERIAL_BAUD);
  delay(200);
  Serial.println("Setup start");

  connectWiFi();
  timeClient.begin();
  timeClient.update();

  if (!vib.begin()) Serial.println("MPU6050 init falhou");
  tempSensor.begin();

  connectMQTT();
  lastPublish = millis() - publishInterval;
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) connectWiFi();
  if (!timeClient.update()) timeClient.forceUpdate();
  if (!mqttClient.connected()) connectMQTT();
  mqttClient.loop();

  unsigned long now = millis();
  if (now - lastPublish >= publishInterval) {
    publish_readings();
    lastPublish = now;
  }
}
