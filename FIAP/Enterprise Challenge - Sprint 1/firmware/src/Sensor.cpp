#include "Sensor.h"
#include <Arduino.h>

SensorData Sensor::read() {
  SensorData d;
  d.timestamp   = millis() / 1000;
  d.temperature = 20.0 + random(0, 600) / 10.0;  // simula
  d.vibration   = random(0, 500) / 100.0;        // simula
  return d;
}
