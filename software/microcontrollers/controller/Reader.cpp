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
  StaticJsonDocument<200> doc;
  String dataFormatted;

  // setting up sensors data
  JsonObject humidity = doc.createNestedObject("humidity");
  humidity["value"] = this->humidity;
  humidity["unit"] = "%";

  JsonObject temperature = doc.createNestedObject("temperature");
  temperature["value"] = this->temperature;
  temperature["unit"] = "Celsius";

  JsonObject raining = doc.createNestedObject("raining");
  raining["value"] = this->isRaining;
  raining["unit"] = "bool";

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
