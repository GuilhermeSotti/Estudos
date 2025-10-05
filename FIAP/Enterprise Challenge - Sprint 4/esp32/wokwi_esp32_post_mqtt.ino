#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

const char* ssid = "YOUR_SSID";
const char* password = "YOUR_PASS";
const char* mqtt_server = "test.mosquitto.org";
const char* mqtt_topic = "factory/sensor/esp01";

WiFiClient espClient;
PubSubClient client(espClient);

void setup_wifi() {
  delay(10);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
}

void reconnect() {
  while (!client.connected()) {
    if (client.connect("esp32_sim")) {
    } else {
      delay(1000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
}

float readTemp() {
  float t = 30 + 10 * sin(millis() / 60000.0);
  t += random(-50,50) / 100.0;
  return t;
}

float readHum(){
  float h = 40 + 15 * cos(millis() / 45000.0);
  h += random(-50,50) / 100.0;
  return h;
}

void loop() {
  if (!client.connected()) reconnect();
  float temp = readTemp();
  float hum = readHum();
  StaticJsonDocument<200> doc;
  doc["device_id"] = "esp01";
  doc["ts"] = millis();
  doc["temp"] = temp;
  doc["hum"] = hum;
  char buffer[256];
  size_t n = serializeJson(doc, buffer);
  client.publish(mqtt_topic, buffer, n);
  Serial.println(buffer);
  client.loop();
  delay(5000);
