#ifndef TEMP_SENSOR_H
#define TEMP_SENSOR_H

#include <Arduino.h>
#include <OneWire.h>
#include <DallasTemperature.h>

class TempSensor {
public:
  TempSensor(uint8_t pinOneWire);
  void begin();
  float read_temperature_c();

private:
  OneWire oneWire;
  DallasTemperature sensors;
  DeviceAddress devAddr;
  bool found = false;
};

#endif
