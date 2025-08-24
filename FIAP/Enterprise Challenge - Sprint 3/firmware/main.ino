#include <Arduino.h>
#include <WiFi.h>
#include <WiFiUdp.h>
#include <NTPClient.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include "esp32_config.h"
#include "vibration_sensor.h"
#include "temp_sensor.h"

#define PIN_DS18B20  15

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
  struct tm * ti;
  ti = gmtime(&raw);
  char buf[32];
  strftime(buf, sizeof(buf), "%Y-%m-%dT%H:%M:%SZ", ti);
  return String(buf);
}

void connectWiFi() {
  Serial.printf("Conectando WiFi: %s\n", WIFI_SSID);
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  unsigned long start = millis();
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    if (millis() - start > 20000) {
      Serial.println("\nFalha WiFi: timeout");
      break;
    }
  }
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWiFi conectado. IP: ");
    Serial.println(WiFi.localIP());
  }
}

void connectMQTT() {
  if (mqttClient.connected()) return;
  Serial.print("Conectando MQTT em ");
  Serial.print(MQTT_BROKER);
  Serial.print(":");
  Serial.println(MQTT_PORT);
  mqttClient.setServer(MQTT_BROKER, MQTT_PORT);
  int tries = 0;
  while (!mqttClient.connected() && tries < 6) {
    String clientId = "ESP32Client-";
    clientId += String((uint32_t)ESP.getEfuseMac(), HEX);
    if (mqttClient.connect(clientId.c_str())) {
      Serial.println("MQTT conectado");
      break;
    } else {
      Serial.print("MQTT falha rc=");
      Serial.print(mqttClient.state());
      Serial.println(", tentando novamente em 2s");
      delay(2000);
      tries++;
    }
  }
}

void setup() {
  Serial.begin(SERIAL_BAUD);
  delay(500);
  Serial.println("=== Iniciando ESP32 - Manutenção Preditiva ===");

  connectWiFi();

  timeClient.begin();
  timeClient.update();

  Serial.println("Inicializando sensor de vibração (MPU6050)...");
  if (!vib.begin()) {
    Serial.println("Falha ao inicializar MPU6050! Verifique conexões I2C.");
  } else {
    Serial.println("MPU6050 pronto.");
  }

  Serial.println("Inicializando sensor de temperatura (DS18B20)...");
  tempSensor.begin();

  connectMQTT();

  lastPublish = millis() - publishInterval;
}

void publish_readings() {
  float vib_g = vib.read_vibration_g();
  float temp_c = tempSensor.read_temperature_c();

  StaticJsonDocument<256> doc;
  doc["machine_id"] = MACHINE_ID;
  doc["timestamp"] = iso8601_now();

  JsonArray sensors = doc.createNestedArray("sensors");
  JsonObject s1 = sensors.createNestedObject();
  s1["type"] = "vibration";
  if (!isnan(vib_g)) {
    s1["value"] = vib_g;
    s1["unit"] = "g";
  } else {
    s1["value"] = nullptr;
  }

  JsonObject s2 = sensors.createNestedObject();
  s2["type"] = "temperature";
  if (!isnan(temp_c)) {
    s2["value"] = temp_c;
    s2["unit"] = "C";
  } else {
    s2["value"] = nullptr;
  }

  char payload[512];
  size_t n = serializeJson(doc, payload, sizeof(payload));
  String topic = String(MQTT_TOPIC_BASE) + "/" + String(MACHINE_ID) + "/sensors";
  Serial.printf("Publicando para %s -> %s\n", topic.c_str(), payload);
  if (!mqttClient.connected()) {
    connectMQTT();
  }
  boolean ok = mqttClient.publish(topic.c_str(), payload, false);
  if (!ok) {
    Serial.println("Falha ao publicar MQTT");
  }
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    connectWiFi();
  }
  if (!timeClient.update()) {
    timeClient.forceUpdate();
  }
  if (!mqttClient.connected()) {
    connectMQTT();
  }
  mqttClient.loop();

  unsigned long now = millis();
  if (now - lastPublish >= publishInterval) {
    publish_readings();
    lastPublish = now;
  }
}
