#ifndef CONFIG_H
#define CONFIG_H

namespace Config {
  constexpr int DHT_PIN         = 4;
  constexpr int LDR_PIN         = 34;
  constexpr int PB_PIN_P        = 12;
  constexpr int PB_PIN_K        = 14;
  constexpr int RELAY_PIN       = 26;
  constexpr int SD_CS_PIN       = 5;

  constexpr unsigned long LOOP_DELAY_MS       = 5000;  // 5s
  constexpr int HUMIDITY_THRESHOLD_DEFAULT   = 30;    // %
  constexpr int MA_WINDOW_SIZE               = 6;     // média móvel (6 leituras ~30s)
}

#endif