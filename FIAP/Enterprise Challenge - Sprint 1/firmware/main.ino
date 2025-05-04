#include <ArduinoJson.h>
#include "Config.h"
#include "WiFiManager.h"
#include "MQTTClient.h"
#include "Sensor.h"

void setup() {
  Serial.begin(115200);
  WiFiManager::begin();
  MQTTClient::begin();
}

void loop() {
  SensorData data = Sensor::read();

  // Serial para debug
  Serial.printf("Temp: %.2f °C, Vib: %.2f\n", data.temperature, data.vibration);

  // Monta JSON
  StaticJsonDocument<200> doc;
  doc["timestamp"]   = data.timestamp;
  doc["temperature"] = data.temperature;
  doc["vibration"]   = data.vibration;
  char buffer[256];
  size_t n = serializeJson(doc, buffer);

  // Publica
  if (MQTTClient::publish(MQTT_TOPIC, buffer)) {
    Serial.println("→ Publicado com sucesso");
  } else {
    Serial.println("! Falha ao publicar");
  }

  MQTTClient::loop();
  delay(1000);
}
