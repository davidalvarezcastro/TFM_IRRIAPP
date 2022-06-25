/**
 * Developer: David Álvarez Castro
 * Mail: davidac0291@gmail.com
 * Date: 24/06/2022
 *
 * Example received data from serial port:
 *  0;{"humidity":{"value":66.56,"unit":"%"},"temperature":{"value":25.22,"unit":"Celsius"},"raining":{"value":false,"unit":"bool"}}
 **/
#include <ESP8266WiFi.h>
#include <SoftwareSerial.h>
#include "pinout.h"
#include "config.h"
#include "SerialReader.h"

// Set up a new SoftwareSerial object
SerialReader reader = SerialReader();

void setup()
{
  reader.init(RX_PIN, TX_PIN);
  Serial.begin(SERIAL_DEFAULT_BAUND);
}

void loop()
{
  // process string received from serial port
  reader.readSerial();
  delay(1000);
}
