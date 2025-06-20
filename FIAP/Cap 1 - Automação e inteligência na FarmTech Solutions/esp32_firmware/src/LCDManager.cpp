#include "LCDManager.h"
#include "Config.h"
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

static LiquidCrystal_I2C lcd(LCD_I2C_ADDR, 16, 2);

void LCDManager::init() {
    Wire.begin(I2C_SDA, I2C_SCL);
    lcd.init();
    lcd.backlight();
    lcd.clear();
}

void LCDManager::display(float moisture, float nutrient) {
    lcd.setCursor(0, 0);
    lcd.print("Umi:");
    lcd.print(moisture, 1);
    lcd.print("%   ");

    lcd.setCursor(0, 1);
    lcd.print("Nut:");
    lcd.print(nutrient, 1);
    lcd.print("%   ");
}
