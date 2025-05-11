#include "MQTTClient.h"
#include "Config.h"
#include <Arduino.h>

WiFiClientSecure MQTTClient::_secureClient;
PubSubClient MQTTClient::_client(_secureClient);

void MQTTClient::begin() {
  _secureClient.setCACert(ROOT_CA_CERT);
  _secureClient.setCertificate(DEVICE_CERT);
  _secureClient.setPrivateKey(PRIVATE_KEY);

  _client.setServer(MQTT_HOST, MQTT_PORT);
  connect();
}

void MQTTClient::connect() {
  while (!_client.connected()) {
    Serial.print("Conectando MQTT...");
    if (_client.connect("ESP32Client")) {
      Serial.println(" conectou!");
    } else {
      Serial.print(" falhou, rc=");
      Serial.print(_client.state());
      Serial.println(" - tentado de novo em 2s");
      delay(2000);
    }
  }
}

bool MQTTClient::publish(const char* topic, const char* payload) {
  if (!_client.connected()) {
    connect();
  }
  return _client.publish(topic, payload);
}

void MQTTClient::loop() {
  _client.loop();
}
