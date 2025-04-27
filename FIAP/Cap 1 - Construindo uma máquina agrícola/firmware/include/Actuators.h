#ifndef ACTUATORS_H
#define ACTUATORS_H

namespace Actuators {
  void init();
  void setRelay(bool on);
  bool getRelayState();
}

#endif
