/**
 * Developer: David Álvarez Castro
 * Mail: davidac0291@gmail.com
 * Date: 24/06/2022
 *
 * Example received data from serial port:
 *  0;68.13;%;15.91;Celsius;0;bool#
 **/
#include <ESP8266WiFi.h>
#include <SoftwareSerial.h>
#include "pinout.h"
#include "config.h"
#include "wifi_utils.hpp"
#include "SerialReader.h"
#include "WrapperMqtt.h"
#include "FormatData.h"

// Set up a new SoftwareSerial object
SoftwareSerial mySerial = SoftwareSerial(RX_PIN, TX_PIN);
SerialReader reader = SerialReader();
WrapperMqtt *mqtt = WrapperMqtt::getInstance();

void setup()
{
  // setting up serials
  mySerial.begin(SERIAL_DEFAULT_BAUND);
  Serial.begin(SERIAL_DEFAULT_BAUND);

  // connect to Wifi
  Serial.println("init wifi...");
  connectWifi(WIFI_SSID, WIFI_PASSWORD);

  // init mqtt
  Serial.println("init mqtt...");
  mqtt->init(MQTT_HOST, MQTT_PORT);
}

void loop()
{
  Serial.println("reading serial...");
  // process string received from serial port
  reader.readSerial(&mySerial);

  // process command
  switch (reader.getCommand().toInt())
  {
  case SEND_DATA_MQTT:
    // send data
    mqtt->startLoop(MQTT_ID, MQTT_USERNAME, MQTT_PASSWORD);

    if (reader.getData().length() > 0)
    {
      mqtt->publish(TOPIC_SEND_DATA, FormatData::formatSensorDataAsJSON(reader.getData()));
    }
    break;

  default:
    Serial.println("unknown command!");
    break;
  }

  delay(50);
}
