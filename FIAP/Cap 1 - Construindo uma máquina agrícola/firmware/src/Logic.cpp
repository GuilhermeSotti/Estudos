#include "Logic.h"

bool Logic::evaluate(const SensorReadings &data) {
  if (data.humidity >= 0 && data.humidity < 30.0f) return true;
  if (data.P_state || data.K_state)              return true;
  return false;
}
