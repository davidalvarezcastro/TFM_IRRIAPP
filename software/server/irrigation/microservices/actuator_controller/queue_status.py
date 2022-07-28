import re
import attr
import json

from domain.messages.topics import TOPIC_AREA_ACTUATOR_RELAY_REGEXP


@attr.s
class QueueState():
    type: str = attr.ib()
    topic: str = attr.ib()
    payload: str = attr.ib()

    def get_area(self) -> str:
        try:
            area = int(re.findall(TOPIC_AREA_ACTUATOR_RELAY_REGEXP, self.topic)[0][0])
        except Exception:
            area = None

        return area

    def get_json(self) -> dict:
        return json.loads(self.payload)

    def get_type(self) -> dict:
        return self.type
