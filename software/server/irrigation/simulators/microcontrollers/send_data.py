"""
    Controller Simulator: sensor data mock

    It does not use any controller/service/wrapper from the app. It is just a small script

    Use example:
        python3 send_data.py \
            --host <host> --port <port> --user <user> --password <password> --summer \
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
TOPIC_SENSOR_DATA = "area/{area}/controller/{controller}/sensors/status"  # change it if it is needed
MODE_SUMMER = 'summer'
MODE_WINTER = 'winter'


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


class SensorDataGenerator():
    def __init__(self, mode: str = MODE_SUMMER) -> None:
        self.mode = mode

    def _generate_random_interval(self, a, b, decimals=2):
        return round(random.uniform(a, b), decimals)

    def _generate_new_temperature(self):
        if self.mode == MODE_SUMMER:
            min_temperature = 25
            max_temperature = 45
        else:
            min_temperature = 0
            max_temperature = 16

        return self._generate_random_interval(
            min_temperature,
            max_temperature
        )

    def _generate_new_humidity(self):
        if self.mode == MODE_SUMMER:
            min_humidity = 13
            max_humidity = 80
        else:
            min_humidity = 75
            max_humidity = 95

        return self._generate_random_interval(
            min_humidity,
            max_humidity
        )

    def _generate_new_raining(self):
        if self.mode == MODE_SUMMER:
            return random.uniform(0, 1) > 0.85
        else:
            return random.uniform(0, 1) > 0.1

    def get_payload(self) -> dict:
        return {
            'id': str(uuid.uuid4()),
            'humidity': {
                'value': self._generate_new_humidity(),
                'unit': "%",
            },
            'temperature': {
                'value': self._generate_new_temperature(),
                'unit': "celsius",
            },
            'raining': {
                'value': self._generate_new_raining(),
                'unit': "bool",
            },
        }


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
        '--summer',
        action="store_const", const=True, default=True, help='mqtt mode'
    )
    parser.add_argument(
        '--area',
        type=int, default=1, help='area'
    )
    parser.add_argument(
        '--controller',
        type=int, default=1, help='controller'
    )

    args = parser.parse_args()


def handler(signum, frame):
    stop_event.set()


if __name__ == '__main__':
    global stop_event
    stop_event = threading.Event()
    signal.signal(signal.SIGINT, handler)

    init_arp_parse()

    client_mqtt = MqttClient(
        host=args.host,
        port=args.port,
        user=args.user,
        password=args.password,
    )

    generator = SensorDataGenerator(
        mode=MODE_SUMMER if args.summer else MODE_WINTER
    )

    while not stop_event.is_set():
        print("Generating new payload...")
        payload = generator.get_payload()
        print(f"\t\t {payload}")

        print("Sending data to mqtt...")
        client_mqtt.pub(
            topic=TOPIC_SENSOR_DATA.format(
                area=args.area,
                controller=args.controller,
            ),
            payload=json.dumps(payload)
        )
        print("\t\tSent! Sleeping...")
        time.sleep(5)
