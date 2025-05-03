#include "Logic.h"
#include "Config.h"
#include <vector>

static std::vector<float> hum_buffer;
bool Logic::rainExpected = false;  // sem previsão de chuva

void Logic::updateMovingAverage(float newHum) {
  if (newHum < 0) return;
  hum_buffer.push_back(newHum);
  if (hum_buffer.size() > Config::MA_WINDOW_SIZE)
    hum_buffer.erase(hum_buffer.begin());
}

int Logic::getThreshold() {
  if (hum_buffer.empty())
    return Config::HUMIDITY_THRESHOLD_DEFAULT;
  float sum = 0;
  for (auto h: hum_buffer) sum += h;
  float avg = sum / hum_buffer.size();
  return static_cast<int>(avg * 0.9f);
}

bool Logic::evaluate(const SensorReadings &data) {
  updateMovingAverage(data.humidity);

  // chuva sempre false → ignora

  int th = getThreshold();
  if (data.humidity >= 0 && data.humidity < th) return true;
  if (data.P_state || data.K_state)              return true;
  return false;
}
