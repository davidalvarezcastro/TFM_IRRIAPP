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
  manager.sendCommand(SEND_DATA_MQTT, Reader::getInstance()->getData());

  // send data to dispatcher
  delay(DELAY_LOOP);
}
