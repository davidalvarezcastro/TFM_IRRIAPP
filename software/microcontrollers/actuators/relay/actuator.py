from mqtt import MQTTManager
from relay import Controller
from globals import TOPIC_CONFIRMATION_TURN_OFF, TOPIC_CONFIRMATION_TURN_ON, TOPIC_TURN_OFF, TOPIC_TURN_ON
from secrets import AREA_ACTUATOR


class Actuator():
    def __init__(self, controller: Controller, mqtt_manager: MQTTManager) -> None:
        self.topic_turn_on = TOPIC_TURN_ON.format(area=AREA_ACTUATOR)
        self.topic_turn_on_ok = TOPIC_CONFIRMATION_TURN_ON.format(area=AREA_ACTUATOR)
        self.topic_turn_off = TOPIC_TURN_OFF.format(area=AREA_ACTUATOR)
        self.topic_turn_off_ok = TOPIC_CONFIRMATION_TURN_OFF.format(area=AREA_ACTUATOR)

        self.mqtt_manager = mqtt_manager
        self.mqtt_manager.set_callback(cb=self._handle_mqtt_events)
        self.mqtt_manager.subscribe(self.topic_turn_on)
        self.mqtt_manager.subscribe(self.topic_turn_off)

        self.controller = controller

    def _handle_mqtt_events(self, topic: bytes, msg: bytes):
        topic = topic.decode("utf-8")
        msg = msg.decode("utf-8")
        print(f"topic received! => {topic}: {msg}")

        if topic == self.topic_turn_on:
            self.controller.on()
            self.mqtt_manager.publish(
                topic=self.topic_turn_on_ok,
                payload=None
            )

        elif topic == self.topic_turn_off:
            self.controller.off()
            self.mqtt_manager.publish(
                topic=self.topic_turn_off_ok,
                payload=None
            )
        else:
            print(f"Topic {topic} unknown")

    def run(self) -> None:
        self.mqtt_manager.run()
