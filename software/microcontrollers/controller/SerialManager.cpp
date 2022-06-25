#include "SerialManager.h"

void SerialManager::init(SoftwareSerial &serial)
{
  serial.begin(SERIAL_DEFAULT_BAUND);
  this->s = &serial;
}

void SerialManager::sendCommand(COMMANDS_DISPATCHER command, String data)
{
  String serialData;
  serialData = String(command) + SERIAL_SEPARATOR_STRING + data + SERIAL_END_STRING;
  Serial.println("\nSending data to wifi manager (dispatcher): \n\t" + serialData + "\n\n");

  this->s->println(serialData);
}
