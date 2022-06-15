/**
  * Developer: David Álvarez Castro
  * Mail: davidac0291@gmail.com
  * Date: 12/06/2022
  **/


// CONSTANTS
#define PIN_HUMIDITY_SENSOR A0
#define PIN_TEMPERATURE_SENSOR A1
#define PIN_RAIN_SENSOR 5

const int delayLoop = 1000;            // 1 second of delay


// GLOBAL VARS
float humidityPercentage;
float temperatureCelsius;
bool isRaining;


void setup()
{
  pinMode(PIN_RAIN_SENSOR, INPUT);
  Serial.begin(9600);
}


void loop()
{
  Serial.println("Reading sensors value...");
  humidityPercentage = readHumidity();
  temperatureCelsius = readTemperature();
  isRaining = readRaining();

  Serial.println("\n");
  Serial.print(humidityPercentage);
  Serial.println(" %\n");

  Serial.print(temperatureCelsius);
  Serial.println(" ºC\n");

  if (isRaining)
  {
    Serial.println("It is raining!");
  }

  delay(delayLoop);
}

/**
 * Function to read temperature sensor
 *
 * @return % of humidity
 */
float readHumidity () {
  int humidityValue = analogRead(PIN_HUMIDITY_SENSOR);
  return 100.0 - (humidityValue / 10.23);
}

/**
 * Function to read humidity sensor
 *
 * @return temperature in Celsius
 */
float readTemperature () {
  int temperatureValue = analogRead(PIN_TEMPERATURE_SENSOR);
  float temperatureMillivolts = (temperatureValue / 1023.0) * 5000;
  return temperatureMillivolts / 10;
}

/**
 * Function to read raining sensor
 *
 * @return is it raining?
 */
bool readRaining () {
  int rainingValue = digitalRead(PIN_RAIN_SENSOR);
  Serial.print(" Raining?: ");
  Serial.print(rainingValue);
  Serial.println("\n");
  return rainingValue == LOW;
}
