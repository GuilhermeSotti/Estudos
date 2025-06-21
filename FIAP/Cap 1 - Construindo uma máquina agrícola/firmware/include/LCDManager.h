#ifndef LCD_MANAGER_H
#define LCD_MANAGER_H

#include <Arduino.h>

class LCDManager {
public:
    static void init();
    static void display(uint8_t moisture, uint8_t nutrient);
};

#endif
