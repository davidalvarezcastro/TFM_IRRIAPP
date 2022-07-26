import json
import machine
import time
from lib.mqtt import MQTTClient

from globals import AREA_ID


class MQTTManager():

    def __init__(self,
                 host: str = "irrigation.gal",
                 port: int = 1883,
                 user: str = "user",
                 password: str = "user") -> Exception:

        self.host = host
        self.port = port
        self.user = user
        self.password = password

        try:
            self.client = MQTTClient(
                AREA_ID,
                server=self.host, port=self.port,
                user=self.user, password=self.password,
                keepalive=300, ssl=False, ssl_params={}
            )
            self.client.connect()
            print('Connected to %s MQTT broker as client ID: %s' % (self.host, AREA_ID))
        except Exception as e:
            self.restart_microcontroller()

    def restart_microcontroller(self) -> None:
        print('Failed to connect to MQTT broker. Reconnecting...')
        time.sleep(10)
        machine.reset()

    def subscribe(self, topic: str) -> None:
        try:
            self.client.subscribe(
                topic=topic
            )
        except Exception as e:
            self.restart_microcontroller()

    def publish(self, topic: str, payload: dict = None) -> None:
        try:
            self.client.publish(
                topic=topic,
                msg=json.dumps(payload).encode('utf-8') if payload is not None else '{}'
            )
        except Exception as e:
            self.restart_microcontroller()

    def set_callback(self, cb) -> None:
        self.client.set_callback(cb)

    def run(self) -> None:
        while True:
            try:
                self.client.wait_msg()
            except Exception as e:
                self.restart_microcontroller()
