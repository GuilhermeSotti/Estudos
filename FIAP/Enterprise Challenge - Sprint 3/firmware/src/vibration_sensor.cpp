#include "vibration_sensor.h"

VibrationSensor::VibrationSensor() {}

bool VibrationSensor::begin() {
  if (!mpu.begin()) {
    return false;
  }
  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_5_HZ);
  delay(100);
  return true;
}

float VibrationSensor::vec_to_g(sensors_event_t* accel) {
  const float g = 9.80665f;
  float ax = accel->acceleration.x;
  float ay = accel->acceleration.y;
  float az = accel->acceleration.z;
  float mag = sqrtf(ax*ax + ay*ay + az*az);
  return mag / g;
}

float VibrationSensor::read_vibration_g() {
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);
  float mag_g = vec_to_g(&a);
  return mag_g;
}
