#ifndef CONFIG
#define CONFIG

// Wifi settings
#define WIFI_SSID "ssid"
#define WIFI_PASSWORD "password"

// MQTT settings
#define MQTT_HOST "host"
#define MQTT_PORT 1883
#define MQTT_USERNAME "username"
#define MQTT_PASSWORD "password"
#define MQTT_ID "id"
#define TOPIC_SEND_DATA "zona/{zona}/controlador/{controlador}/sensores/estado"

// serial settings
#define SERIAL_DEFAULT_BAUND 9600
#define SERIAL_SEPARATOR_STRING ';'
#define SERIAL_END_STRING '#'

#endif
