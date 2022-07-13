#include "Reader.h"

Reader *Reader::getInstance()
{
  static Reader instance;
  return &instance;
}

void Reader::readSensors()
{
  Serial.println("Reading sensors value...");
  this->readHumidity();
  this->readTemperature();
  this->readRaining();
}

String Reader::getData()
{
  String dataFormatted = "";

  // setting up sensors data
  dataFormatted += String(this->humidity) + SERIAL_SEPARATOR_STRING + "%";
  dataFormatted += SERIAL_SEPARATOR_STRING + String(this->temperature) + SERIAL_SEPARATOR_STRING + "Celsius";
  dataFormatted += SERIAL_SEPARATOR_STRING + String(this->isRaining) + SERIAL_SEPARATOR_STRING + "bool";

  return dataFormatted;
}

void Reader::readHumidity()
{
  int humidityValue = analogRead(PIN_HUMIDITY_SENSOR);
  this->humidity = 100.0 - (humidityValue / 10.23);

  this->printHumidity();
}

void Reader::readTemperature()
{
  int temperatureValue = analogRead(PIN_TEMPERATURE_SENSOR);
  float temperatureMillivolts = (temperatureValue / 1023.0) * 5000;
  this->temperature = temperatureMillivolts / 10;

  this->printTemperature();
}

void Reader::readRaining()
{
  int rainingValue = digitalRead(PIN_RAIN_SENSOR);
  Serial.print(" Raining?: ");
  Serial.print(rainingValue);
  Serial.println("\n");
  this->isRaining = rainingValue == LOW;

  this->printRaining();
}
