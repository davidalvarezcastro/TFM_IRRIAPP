import re
import attr
import json

from domain.messages.topics import TOPIC_AREA_SENSORS_STATUS_CONTROLLER_REGEXP


@attr.s
class QueueState():
    topic: str = attr.ib()
    payload: str = attr.ib()

    def get_area(self) -> str:
        try:
            area = int(re.findall(TOPIC_AREA_SENSORS_STATUS_CONTROLLER_REGEXP, self.topic)[0][0])
        except Exception:
            area = None

        return area

    def get_controlller(self) -> str:
        try:
            controller = int(re.findall(TOPIC_AREA_SENSORS_STATUS_CONTROLLER_REGEXP, self.topic)[0][1])
        except Exception:
            controller = None

        return controller

    def get_json(self) -> dict:
        return json.loads(self.payload)
