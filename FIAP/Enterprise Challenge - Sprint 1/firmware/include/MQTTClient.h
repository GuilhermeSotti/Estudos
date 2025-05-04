#ifndef MQTT_CLIENT_H
#define MQTT_CLIENT_H

#include <PubSubClient.h>
#include <WiFiClientSecure.h>

class MQTTClient {
  public:
    static void begin();
    static bool publish(const char* topic, const char* payload);
    static void loop();
  private:
    static PubSubClient _client;
    static WiFiClientSecure _secureClient;
    static void connect();
};

#endif // MQTT_CLIENT_H
