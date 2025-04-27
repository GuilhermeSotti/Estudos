#include "Actuators.h"
#include "Config.h"
#include <Arduino.h>

static bool relayState = false;

void Actuators::init() {
  pinMode(Config::RELAY_PIN, OUTPUT);
  digitalWrite(Config::RELAY_PIN, HIGH);
}

void Actuators::setRelay(bool on) {
  relayState = on;
  digitalWrite(Config::RELAY_PIN, on ? LOW : HIGH);
}

bool Actuators::getRelayState() {
  return relayState;
}