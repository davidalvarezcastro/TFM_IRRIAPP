'''
    Main file:
        set up network connection
        set up mqtt broker connectior
        run actuator algorithm: receive command and response ok (by using events)
'''
from mqtt import MQTTManager
from relay import RelayController
from mynetwork import NetworkManager
from secrets import WIFI_SETTINGS, MQTT_SETTINGS

from actuator import Actuator
from globals import PINOUT_RELAY


if __name__ == "__main__":
    controller = RelayController(pinout=PINOUT_RELAY)
    network_manager = NetworkManager(ssid=WIFI_SETTINGS.get('ssid'), pw=WIFI_SETTINGS.get('password'))
    network_manager.connect()

    mqtt_manager = MQTTManager(
        host=MQTT_SETTINGS.get('host'),
        port=MQTT_SETTINGS.get('port'),
        user=MQTT_SETTINGS.get('username'),
        password=MQTT_SETTINGS.get('password'),
    )

    actuator = Actuator(
        controller=controller,
        mqtt_manager=mqtt_manager,
    )
    actuator.run()
