#ifndef CONFIG_H
#define CONFIG_H

namespace Config {
  constexpr int DHT_PIN         = 4;     // GPIO4 para DHT22
  constexpr int LDR_PIN         = 34;    // GPIO34 para LDR (pH)
  constexpr int PB_PIN_P        = 12;    // GPIO12 para botão P
  constexpr int PB_PIN_K        = 14;    // GPIO14 para botão K
  constexpr int RELAY_PIN       = 26;    // GPIO26 para relé (bomba)
  constexpr unsigned long LOOP_DELAY_MS = 5000; // intervalo de loop em ms
}

#endif
