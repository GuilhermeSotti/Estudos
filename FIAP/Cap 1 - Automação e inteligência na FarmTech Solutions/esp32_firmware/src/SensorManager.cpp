#include "SensorManager.h"
#include "Config.h"

void SensorManager::init() {
    analogReadResolution(12);
    analogSetAttenuation(ADC_11db);
}

float SensorManager::readSoilMoisture() {
    uint16_t raw = analogRead(PIN_SOIL_MOISTURE);
    float pct = raw * MOISTURE_SCALE;
    return pct;
}

float SensorManager::readNutrientLevel() {
    uint16_t raw = analogRead(PIN_NUTRIENT);
    float pct = raw * NUTRIENT_SCALE;
    return pct;
}
