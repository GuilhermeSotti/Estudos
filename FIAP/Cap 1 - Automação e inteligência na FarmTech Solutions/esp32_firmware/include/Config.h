#ifndef CONFIG_H
#define CONFIG_H

static const uint32_t READ_INTERVAL_MS = 2000;

static const uint8_t PIN_SOIL_MOISTURE = 34; 
static const uint8_t PIN_NUTRIENT       = 35;

static const uint8_t I2C_SDA = 21;
static const uint8_t I2C_SCL = 22;
static const uint8_t LCD_I2C_ADDR = 0x27;

static const uint16_t ADC_MAX = 4095;

static const float MOISTURE_SCALE   = 100.0f / ADC_MAX; 
static const float NUTRIENT_SCALE   = 100.0f / ADC_MAX; 

#endif
