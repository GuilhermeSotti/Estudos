#ifndef VIBRATION_SENSOR_H
#define VIBRATION_SENSOR_H

#include <Arduino.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

class VibrationSensor {
public:
  VibrationSensor();
  bool begin();
  float read_vibration_g();
private:
  Adafruit_MPU6050 mpu;
  float vec_to_g(sensors_event_t* accel);
};

#endif