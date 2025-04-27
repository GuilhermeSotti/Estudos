#include "Sensors.h"
#include "Config.h"
#include <DHT.h>
#include <Arduino.h>

#define DHTTYPE DHT22
static DHT dht(Config::DHT_PIN, DHTTYPE);

void Sensors::init() {
  dht.begin();
  pinMode(Config::PB_PIN_P, INPUT_PULLUP);
  pinMode(Config::PB_PIN_K, INPUT_PULLUP);
}

SensorReadings Sensors::readAll() {
  SensorReadings data;
  data.P_state  = (digitalRead(Config::PB_PIN_P) == LOW);
  data.K_state  = (digitalRead(Config::PB_PIN_K) == LOW);

  int ldr_raw = analogRead(Config::LDR_PIN);
  data.pH     = map(ldr_raw, 0, 4095, 0, 14);

  float hum = dht.readHumidity();
  data.humidity = isnan(hum) ? -1.0f : hum;

  return data;
}