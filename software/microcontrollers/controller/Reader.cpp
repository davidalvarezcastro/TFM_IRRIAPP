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

String Reader::getDataHumidity()
{
  StaticJsonDocument<50> doc;
  String dataFormatted;

  // setting up sensors data
  doc["value"] = this->humidity;
  doc["unit"] = "%";

  // return data as stringify json
  serializeJson(doc, dataFormatted);
  return dataFormatted;
}

String Reader::getDataTemperature()
{
  StaticJsonDocument<50> doc;
  String dataFormatted;

  // setting up sensors data
  doc["value"] = this->temperature;
  doc["unit"] = "Celsius";

  // return data as stringify json
  serializeJson(doc, dataFormatted);
  return dataFormatted;
}

String Reader::getDataRaining()
{
  StaticJsonDocument<50> doc;
  String dataFormatted;

  // setting up sensors data
  doc["value"] = this->isRaining;
  doc["unit"] = "bool";

  // return data as stringify json
  serializeJson(doc, dataFormatted);
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
  this->isRaining == LOW;

  this->printRaining();
}
