#include "WiFiManager.h"
#include <WiFi.h>
#include <Arduino.h>
#include "Config.h"

void WiFiManager::begin() {
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Conectando à rede WiFi");
  unsigned long start = millis();
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    if (millis() - start > 20000) {
      Serial.println("\nFalha ao conectar WiFi");
      return;
    }
  }
  Serial.println("\nWiFi conectado!");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());
}
