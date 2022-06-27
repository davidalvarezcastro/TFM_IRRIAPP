#ifndef WRAPPERMQTT
#define QRAPPERMQTT

#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <SoftwareSerial.h>
#include "pinout.h"
#include "config.h"
#include "commands.h"

class WrapperMqtt
{
public:
  /**
   * Singleton Pattern
   */
  static WrapperMqtt *getInstance(); // Accessor for singleton instance

  /**
   * Set up mqtt client
   *
   * @param {String} host
   * @param {int} port
   */
  void init(String host, int port);

  /**
   * Init loop mqtt client
   *
   * @param {String} name id
   * @param {String} username
   * @param {int} password
   */
  void startLoop(String name, String username, String password);

  /**
   * Function to publish data to MQTT
   *
   * @param {String} topic
   * @param {String} payload data to be sent to mqtt broker
   * @param {int} qos quality of service
   */
  void publish(String topic, String payload);

private:
  WrapperMqtt() = default; // Make constructor private
  IPAddress host;
  int port;
  WiFiClient espClient;
  PubSubClient mqttClient;

  /**
   * Connect to broker
   *
   * @param {String} name id
   * @param {String} username
   * @param {String} password
   */
  void connect(String name, String username, String password)
  {
    while (!this->mqttClient.connected())
    {
      Serial.print("Starting MQTT connection...");
      if (this->mqttClient.connect(name.c_str(), username.c_str(), password.c_str()))
      {
        Serial.print("MQTT connected!");
      }
      else
      {
        Serial.print("Failed MQTT connection, rc=");
        Serial.print(this->mqttClient.state());
        Serial.println(" try again in 5 seconds");
        delay(5000);
      }
    }
  }

  /**
   * Function to print some info after receiving a msg
   */
  static void OnMqttReceived(char *topic, byte *payload, unsigned int length)
  {
    Serial.print("Received on ");
    Serial.print(topic);
    Serial.print(": ");

    String content = "";
    for (size_t i = 0; i < length; i++)
    {
      content.concat((char)payload[i]);
    }
    Serial.print(content);
    Serial.println();
  }
};

#endif
