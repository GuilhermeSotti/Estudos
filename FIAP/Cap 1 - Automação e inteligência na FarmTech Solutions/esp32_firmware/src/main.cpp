#include <Arduino.h>
#include "Config.h"
#include "SensorManager.h"
#include "LCDManager.h"

void setup() {
    Serial.begin(115200);
    SensorManager::init();
    LCDManager::init();
}

void loop() {
    float umidade   = SensorManager::readSoilMoisture();
    float nutriente = SensorManager::readNutrientLevel();

    Serial.println(umidade);

    Serial.print("{\"umidade\":");
    Serial.print(umidade, 2);
    Serial.print(",\"nutriente\":");
    Serial.print(nutriente, 2);
    Serial.println("}");

    LCDManager::display(umidade, nutriente);

    delay(READ_INTERVAL_MS);
}
