"""
    Actuator Simulator: relay management mock

    It does not use any controller/service/wrapper from the app. It is just a small script

    Use example:
        python3 actuator.py \
            --host <host> --port <port> --user <user> --password <password> \
            --area <area> --controller <controller>
"""
import argparse
import json
import random
import signal
import threading
import time
import uuid
import paho.mqtt.client

# globals
TOPIC_AREA_ACTUATOR_RELAY_ON = "area/{area}/actuator/on"
TOPIC_AREA_ACTUATOR_RELAY_ON_CONFIRMATION = "area/{area}/actuator/on/ok"
TOPIC_AREA_ACTUATOR_RELAY_OFF = "area/{area}/actuator/off"
TOPIC_AREA_ACTUATOR_RELAY_OFF_CONFIRMATION = "area/{area}/actuator/off/ok"


class MqttClient:
    """ Simple client mqtt wrapper for sending data
    """

    def __init__(self, host: str, port: int, user: str, password: str):
        self.client = paho.mqtt.client.Client(
            client_id=f"simulator_send_data_{uuid.uuid4()}",
            protocol=paho.mqtt.client.MQTTv311,
            transport='tcp',
        )
        self.client.username_pw_set(user, password)

        self.client.connect(host, port=port)
        self.client.loop_start()

    def pub(self, topic, payload, qos=1, wait_for_publish=True, exception=True):
        status = self.client.publish(topic=topic, payload=payload, qos=1)
        if status.rc == paho.mqtt.client.MQTT_ERR_NO_CONN:
            if exception:
                raise Exception(paho.mqtt.client.error_string(status.rc))
        if wait_for_publish:
            status.wait_for_publish()

    def sub(self, topic, function, qos=1):
        try:
            self.client.subscribe(topic)
            self.client.message_callback_add(topic, function)
        except Exception:
            pass


def init_arp_parse():
    global args

    parser = argparse.ArgumentParser(
        description='Sensor data controller simulator. Just send sensor data to mqtt!')
    parser.add_argument(
        '--host',
        type=str, default="localhost", help='mqtt host'
    )
    parser.add_argument(
        '--port',
        type=int, default=1883, help='mqtt port'
    )
    parser.add_argument(
        '--user',
        type=str, default="user", help='mqtt user'
    )
    parser.add_argument(
        '--password',
        type=str, default="admin", help='mqtt password'
    )
    parser.add_argument(
        '--area',
        type=int, default=1, help='area'
    )

    args = parser.parse_args()


def handler(signum, frame):
    stop_event.set()


def handler_relay_on(client, userdata: dict, mensaje) -> None:
    client_mqtt.pub(
        topic=TOPIC_AREA_ACTUATOR_RELAY_ON_CONFIRMATION.format(
            area=args.area
        ),
        payload=json.dumps({}),
        wait_for_publish=False
    )


def handler_relay_off(client, userdata: dict, mensaje) -> None:
    client_mqtt.pub(
        topic=TOPIC_AREA_ACTUATOR_RELAY_OFF_CONFIRMATION.format(
            area=args.area
        ),
        payload=json.dumps({}),
        wait_for_publish=False
    )


if __name__ == '__main__':
    global stop_event, client_mqtt
    stop_event = threading.Event()
    signal.signal(signal.SIGINT, handler)

    init_arp_parse()

    client_mqtt = MqttClient(
        host=args.host,
        port=args.port,
        user=args.user,
        password=args.password,
    )

    client_mqtt.sub(
        topic=TOPIC_AREA_ACTUATOR_RELAY_ON.format(
            area=args.area
        ),
        function=handler_relay_on
    )

    client_mqtt.sub(
        topic=TOPIC_AREA_ACTUATOR_RELAY_OFF.format(
            area=args.area
        ),
        function=handler_relay_off
    )

    while not stop_event.is_set():
        time.sleep(5)
