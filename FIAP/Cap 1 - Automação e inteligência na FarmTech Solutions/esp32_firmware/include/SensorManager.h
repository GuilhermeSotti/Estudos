#ifndef SENSOR_MANAGER_H
#define SENSOR_MANAGER_H

#include <Arduino.h>

class SensorManager {
public:
    static void init();
    static float readSoilMoisture();
    static float readNutrientLevel();
};

#endif
