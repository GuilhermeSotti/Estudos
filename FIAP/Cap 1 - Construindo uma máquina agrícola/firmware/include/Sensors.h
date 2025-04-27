#ifndef SENSORS_H
#define SENSORS_H

#include "Config.h"

struct SensorReadings {
  bool   P_state;
  bool   K_state;
  float  pH;
  float  humidity;
};

namespace Sensors {
  void init();
  SensorReadings readAll();
}

#endif
