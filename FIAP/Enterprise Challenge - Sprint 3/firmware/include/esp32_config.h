#ifndef ESP32_CONFIG_H
#define ESP32_CONFIG_H

#define WIFI_SSID "YOUR_SSID"
#define WIFI_PASS "YOUR_PASSWORD"

#define MQTT_BROKER "192.168.1.100"
#define MQTT_PORT 1883
#define MQTT_TOPIC_BASE "factory/machine"

#define MACHINE_ID "1"

#define PUBLISH_INTERVAL_MS 60000

#define NTP_POOL "pool.ntp.org"
#define NTP_OFFSET_SECS 0
#define NTP_INTERVAL_SECS 60000

#define SERIAL_BAUD 115200

#endif
