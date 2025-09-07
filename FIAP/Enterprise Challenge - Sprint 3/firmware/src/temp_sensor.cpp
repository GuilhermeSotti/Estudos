#include "temp_sensor.h"

TempSensor::TempSensor(uint8_t pinOneWire) : oneWire(pinOneWire), sensors(&oneWire) {}

void TempSensor::begin() {
  sensors.begin();
  if (sensors.getDeviceCount() > 0) {
    DeviceAddress addr;
    if (sensors.getAddress(addr, 0)) {
      memcpy(devAddr, addr, sizeof(DeviceAddress));
      found = true;
      sensors.setResolution(devAddr, 12);
    } else {
      found = false;
    }
  } else {
    found = false;
  }
}

float TempSensor::read_temperature_c() {
  if (!found) {
    sensors.begin();
    if (sensors.getDeviceCount() == 0) {
      return NAN;
    }
    if (!sensors.getAddress(devAddr, 0)) return NAN;
    found = true;
  }
  sensors.requestTemperatures();
  float t = sensors.getTempC(devAddr);
  if (t == DEVICE_DISCONNECTED_C) return NAN;
  return t;
}
