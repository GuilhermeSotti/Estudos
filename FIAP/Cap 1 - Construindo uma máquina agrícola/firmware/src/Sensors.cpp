#include "Sensors.h"
#include <DHT.h>
#include <Arduino.h>

#define DHTTYPE DHT22
static DHT dht(Config::DHT_PIN, DHTTYPE);

void Sensors::init() {
  dht.begin();
  pinMode(Config::PB_PIN_P, INPUT_PULLUP);
  pinMode(Config::PB_PIN_K, INPUT_PULLUP);
  if (!SD.begin(Config::SD_CS_PIN)) {
    Serial.println("Erro: SD nao inicializada!");
  }
}

SensorReadings Sensors::readAll() {
  SensorReadings data;
  data.P_state  = (digitalRead(Config::PB_PIN_P) == LOW);
  data.K_state  = (digitalRead(Config::PB_PIN_K) == LOW);

  int ldr_raw = analogRead(Config::LDR_PIN);
  data.pH = map(ldr_raw, 0, 4095, 0, 14);

  float hum = dht.readHumidity();
  if (isnan(hum)) {
    data.humidity = -1.0f;
    data.dht_error = true;
  } else {
    data.humidity = hum;
    data.dht_error = false;
  }

  return data;
}
