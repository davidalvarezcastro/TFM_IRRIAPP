#include <SoftwareSerial.h>
#include "SerialReader.h"

void SerialReader::readSerial(SoftwareSerial *s)
{
  // reset
  this->command = "";
  this->data = "";

  if (s->available() > 0)
  {
    while (s->available() > 0)
    {
      this->command = s->readStringUntil(SERIAL_SEPARATOR_STRING);
      this->data = s->readStringUntil(SERIAL_END_STRING);
    }
  }
}

String SerialReader::getCommand()
{
  return this->command;
}

String SerialReader::getData()
{
  return this->data;
}
