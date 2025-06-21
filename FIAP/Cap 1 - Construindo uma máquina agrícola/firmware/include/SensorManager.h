#ifndef SENSOR_MANAGER_H
#define SENSOR_MANAGER_H

#include <Arduino.h>

class SensorManager {
public:
    static void init();
    static uint8_t readSoilMoisture();
    static uint8_t readNutrientLevel();
};

#endif
