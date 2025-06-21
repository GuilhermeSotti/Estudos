#include "SensorManager.h"
#include "Config.h"
#include <Arduino.h>

void SensorManager::init() {
    analogReadResolution(12);
    analogSetAttenuation(ADC_11db);
}

uint8_t SensorManager::readSoilMoisture() {
    uint16_t raw = analogRead(PIN_SOIL_MOISTURE);
    uint8_t pct = (uint32_t(raw) * 100u) / ADC_MAX;
    return pct;
}

uint8_t SensorManager::readNutrientLevel() {
    uint16_t raw = analogRead(PIN_NUTRIENT);
    uint8_t pct = (uint32_t(raw) * 100u) / ADC_MAX;
    return pct;
}
