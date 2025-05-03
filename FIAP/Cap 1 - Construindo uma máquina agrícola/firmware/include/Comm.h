#ifndef COMM_H
#define COMM_H

#include "Sensors.h"

namespace Comm {
  void init();
  void sendJSON(const SensorReadings &data, bool relayState);
}

#endif
