#include <SoftwareSerial.h>
#include "SerialReader.h"

void SerialReader::init(int pinRx, int pinTx)
{
  SoftwareSerial a = SoftwareSerial(pinRx, pinTx);
  this->s = &a;
  this->s->begin(SERIAL_DEFAULT_BAUND);
}

void SerialReader::readSerial()
{
  // reset
  this->command = "";
  this->data = "";

  if (this->s->available() > 0)
  {
    while (this->s->available() > 0)
    {
      this->command = Serial.readStringUntil(SERIAL_SEPARATOR_STRING);
      this->data = Serial.readStringUntil(SERIAL_END_STRING);
    }
  }

  Serial.println(this->command);
  Serial.println(this->data);
}

String SerialReader::getCommand()
{
  return this->command;
}

String SerialReader::getData()
{
  return this->data;
}
