#ifndef CONFIG
#define CONFIG

// Wifi settings
#define SSID "ssid"
#define PASSWORD "password"
#define HOSTNAME "controller-1"

#define WIFI_IP "192.168.1.200"
#define WIFI_GATEWAY "192.168.1.1"
#define WIFI_SUBNET "255.255.255.0"

// MQTT settings
#define MQTT_HOST "192.168.1.150"
#define MQTT_PORT 1883

// serial settings
#define SERIAL_DEFAULT_BAUND 9600
#define SERIAL_SEPARATOR_STRING ';'
#define SERIAL_END_STRING '\n'

#endif
