#ifndef READER
#define READER

#include <Arduino.h>
#include <SoftwareSerial.h>
#include "./libraries/ArduinoJson.h"
#include "pinout.h"

class Reader
{
public:
  /**
   * Singleton Pattern
   */
  static Reader *getInstance(); // Accessor for singleton instance

  /**
   * Function to read all sensors
   */
  void readSensors();

  /**
   * Function to get sensors data formatted
   *
   * @return String sensor data formatted as json (string)
   */
  String getData();

private:
  Reader() = default; // Make constructor private
  float humidity;
  float temperature;
  bool isRaining;

  /**
   * Function to read temperature sensor
   *
   * % of humidity
   */
  void readHumidity();

  /**
   * Function to read humidity sensor
   *
   * temperature in Celsius
   */
  void readTemperature();

  /**
   * Function to read raining sensor
   *
   * is it raining?
   */
  void readRaining();

  /**
   * Function to print humidity data sensor
   */
  void printHumidity()
  {
    Serial.println("\n");
    Serial.print(this->humidity);
    Serial.println(" %\n");
  }

  /**
   * Function to print temperature data sensor
   */
  void printTemperature()
  {
    Serial.print(this->temperature);
    Serial.println(" ºC\n");
  }

  /**
   * Function to print raining data sensor
   */
  void printRaining()
  {
    if (this->isRaining)
    {
      Serial.println("It is raining!");
    }
  }
};

#endif
