#ifndef SENSORS_H
#define SENSORS_H

#include "Config.h"
#include <SD.h>

struct SensorReadings {
  bool   P_state;
  bool   K_state;
  float  pH;
  float  humidity;
  bool   dht_error;
};

namespace Sensors {
  void init();
  SensorReadings readAll();
}

#endif