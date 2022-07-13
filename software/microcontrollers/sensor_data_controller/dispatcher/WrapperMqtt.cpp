#include "WrapperMqtt.h"

WrapperMqtt *WrapperMqtt::getInstance()
{
  static WrapperMqtt instance;
  return &instance;
}

void WrapperMqtt::startLoop(String id, String username, String password)
{
  if (!this->mqttClient.connected())
  {
    this->connect(id, username, password);
  }
  this->mqttClient.loop();
}

void WrapperMqtt::init(String host, int port)
{
  this->port = port;
  this->host.fromString(host);

  this->mqttClient.setClient(this->espClient);
  this->mqttClient.setCallback(WrapperMqtt::OnMqttReceived);
  this->mqttClient.setServer(this->host, this->port);
}

void WrapperMqtt::publish(String topic, String payload)
{
  this->mqttClient.publish(topic.c_str(), (char *)payload.c_str());
}
