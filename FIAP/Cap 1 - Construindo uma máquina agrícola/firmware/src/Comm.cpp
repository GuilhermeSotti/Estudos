#include "Comm.h"
#include <ArduinoJson.h>
#include <Arduino.h>

void Comm::sendJSON(const SensorReadings &data, bool relayState) {
  StaticJsonDocument<256> doc;
  doc["timestamp"] = millis();
  JsonObject sensors = doc.createNestedObject("sensors");
  sensors["P"]        = data.P_state;
  sensors["K"]        = data.K_state;
  sensors["pH"]       = data.pH;
  sensors["humidity"] = data.humidity;
  doc["relay"]        = relayState;

  serializeJson(doc, Serial);
  Serial.println();
}