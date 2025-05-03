#ifndef LOGIC_H
#define LOGIC_H

#include "Sensors.h"

namespace Logic {
  bool evaluate(const SensorReadings &data);
  void updateMovingAverage(float newHum);
  int  getThreshold();
  extern bool rainExpected;  // sempre false agora
}

#endif
