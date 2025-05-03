#include "Comm.h"
#include "Config.h"
#include <ArduinoJson.h>
#include <Arduino.h>
#include <SD.h>

void Comm::init() {
  // nada além de Serial e SD já inicializados em Sensors::init()
}

void Comm::sendJSON(const SensorReadings &data, bool relayState) {
  // 1) Alerta de diagnóstico
  if (data.dht_error) {
    Serial.println("Alerta: Falha no sensor DHT22!");
  }

  // 2) Serial JSON
  StaticJsonDocument<256> doc;
  doc["timestamp"] = millis();
  auto sensors = doc.createNestedObject("sensors");
  sensors["P"]        = data.P_state;
  sensors["K"]        = data.K_state;
  sensors["pH"]       = data.pH;
  sensors["humidity"] = data.humidity;
  doc["relay"] = relayState;
  serializeJson(doc, Serial);
  Serial.println();

  // 3) SD log (CSV)
  File f = SD.open("/log.csv", FILE_APPEND);
  if (f) {
    f.print(millis());     f.print(',');
    f.print(data.P_state); f.print(',');
    f.print(data.K_state); f.print(',');
    f.print(data.pH);      f.print(',');
    f.print(data.humidity);f.print(',');
    f.println(relayState);
    f.close();
  }
}
