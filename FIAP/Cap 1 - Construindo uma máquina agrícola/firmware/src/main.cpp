#include <Arduino.h>
#include "Config.h"
#include "Sensors.h"
#include "Actuators.h"
#include "Logic.h"
#include "Comm.h"

void setup() {
  Serial.begin(115200);
  delay(1000);
  Sensors::init();
  Actuators::init();
  Comm::init();
}

void loop() {
  auto data = Sensors::readAll();
  bool irrigate = Logic::evaluate(data);
  Actuators::setRelay(irrigate);
  Comm::sendJSON(data, irrigate);
  delay(Config::LOOP_DELAY_MS);
}
