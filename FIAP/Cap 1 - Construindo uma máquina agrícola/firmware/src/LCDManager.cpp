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

void LCDManager::display(uint8_t moisture, uint8_t nutrient) {
    lcd.setCursor(0, 0);
    lcd.print(F("Umi:"));
    lcd.print(moisture);
    lcd.print(F("%   "));
    lcd.setCursor(0, 1);
    lcd.print(F("Nut:"));
    lcd.print(nutrient);
    lcd.print(F("%   "));

}
