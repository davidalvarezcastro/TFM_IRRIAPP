/**
 * Developer: David Álvarez Castro
 * Mail: davidac0291@gmail.com
 * Date: 24/06/2022
 **/
#include <SoftwareSerial.h>

#include "config.h"
#include "pinout.h"
#include "commands.h"
#include "Reader.h"
#include "SerialManager.h"

// variables
SoftwareSerial mySerial = SoftwareSerial(RX_PIN, TX_PIN);
SerialManager manager = SerialManager();

void setup()
{
  pinMode(PIN_RAIN_SENSOR, INPUT);
  manager.init(mySerial);
  Serial.begin(SERIAL_DEFAULT_BAUND);
}

void loop()
{
  // read data from connected sensors
  Reader::getInstance()->readSensors();

  // send data to dispatcher
  manager.sendCommand(SEND_HUMIDITY_MQTT, Reader::getInstance()->getDataHumidity());
  manager.sendCommand(SEND_TEMPERATURE_MQTT, Reader::getInstance()->getDataTemperature());
  manager.sendCommand(SEND_RAINING_MQTT, Reader::getInstance()->getDataRaining());

  delay(DELAY_LOOP);
}
