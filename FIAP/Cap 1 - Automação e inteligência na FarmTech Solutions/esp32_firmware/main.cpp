#include <Arduino.h>
#include "Config.h"
#include "SensorManager.h"
#include "LCDManager.h"

void printForPlotter(uint8_t umid, uint8_t nutr) {
    Serial.print(F("umidade:"));
    Serial.println(umid);
    Serial.print(F("nutriente:"));
    Serial.println(nutr);
}

void setup() {
    Serial.begin(115200);

    SensorManager::init();
    LCDManager::init();
}

void loop() {
    uint8_t umidade = SensorManager::readSoilMoisture();
    uint8_t nutriente = SensorManager::readNutrientLevel();

    printForPlotter(umidade, nutriente);

    char buf[64];
    int n = snprintf(buf, sizeof(buf),
                     "{\"umidade\":%u,\"nutriente\":%u}", umidade, nutriente);
    if (n > 0 && n < int(sizeof(buf))) {
        Serial.println(buf);
    } else {
        Serial.println(F("{\"umidade\":0,\"nutriente\":0}"));
    }

    LCDManager::display(umidade, nutriente);

    delay(READ_INTERVAL_MS);
}
