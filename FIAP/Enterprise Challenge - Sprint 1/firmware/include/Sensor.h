#ifndef SENSOR_H
#define SENSOR_H

struct SensorData {
  long timestamp;
  float temperature;
  float vibration;
};

class Sensor {
  public:
    static SensorData read();
};

#endif // SENSOR_H
