#ifndef SERIALMANAGER
#define SERIALMANAGER

#include <Arduino.h>
#include <SoftwareSerial.h>
#include "pinout.h"
#include "config.h"
#include "commands.h"

class SerialManager
{
public:
  /**
   * Initialize serial instance
   */
  void init(SoftwareSerial &serial);

  /**
   * Function to send data to Wifi Communication Controller
   *
   * @param {COMMANDS_DISPATCHER} command
   * @param {String} data
   */
  virtual void sendCommand(COMMANDS_DISPATCHER command, String data);

private:
  SoftwareSerial *s;
};

#endif
