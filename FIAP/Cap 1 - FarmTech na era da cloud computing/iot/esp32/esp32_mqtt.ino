#include <WiFi.h>
#include <PubSubClient.h>
#include "DHT.h"

#define DHTPIN 4
#define DHTTYPE DHT11

const char* WIFI_SSID = "SEU_SSID";
const char* WIFI_PASS = "SUA_SENHA";

const char* MQTT_SERVER = "broker.hivemq.com";
const int MQTT_PORT = 1883;
const char* MQTT_TOPIC = "farmtech/sensors";

WiFiClient espClient;
PubSubClient client(espClient);
DHT dht(DHTPIN, DHTTYPE);

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Conectando a ");
  Serial.println(WIFI_SSID);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi conectado");
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Conectando MQTT...");
    if (client.connect("ESP32FarmTech")) {
      Serial.println("conectado");
    } else {
      Serial.print("falhou, rc=");
      Serial.print(client.state());
      Serial.println(" tentando novamente em 5s");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  dht.begin();
  setup_wifi();
  client.setServer(MQTT_SERVER, MQTT_PORT);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  float temp = dht.readTemperature();
  float hum = dht.readHumidity();
  int soil_raw = analogRead(34);
  float soil_percent = map(soil_raw, 0, 4095, 100, 0); 

  String payload = "{";
  payload += "\"temperatura_a_2_m\":" + String(temp, 2) + ",";
  payload += "\"umidade_relativa_a_2_m\":" + String(hum, 2) + ",";
  payload += "\"soil_percent\":" + String(soil_percent, 1);
  payload += "}";

  Serial.print("Publicando: ");
  Serial.println(payload);
  client.publish(MQTT_TOPIC, payload.c_str());
  delay(60000);
}
