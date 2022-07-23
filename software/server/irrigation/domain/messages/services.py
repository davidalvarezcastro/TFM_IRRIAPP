# coding=utf-8
import attr
import json
from abc import ABC, abstractmethod

from . import topics as topics
from domain.messages.wrapper import MessagesClientWrapper


class MessagesInterface(ABC):
    """
    Communication interface to the events server
    """

    @abstractmethod
    def pub_sensors_status_controllers(self, area: str, controller: str,
                                       payload: dict = None, qos: int = 1, wait_for_publish: bool = False) -> None:
        """
        Function to emit a status event from the sensors controller

        Args:
            area (str): area id
            controller (str): controller id
            payload (dict)
            qos (int)
            wait_for_publish (bool)
        Raise:
            Exception
        """
        raise Exception("NotImplementedException")

    @abstractmethod
    def sub_sensors_status_controllers(self, callback, qos: int = 1) -> None:
        """
         Function to subscribe to the status event from the sensors controller

        Args:
            callback (Function)
            qos (int)
        Raise:
            Exception
        """
        raise Exception("NotImplementedException")


@attr.s
class MessagesServices(MessagesInterface):
    messages_client: MessagesClientWrapper = attr.ib()

    # PUB METHODS
    def pub_sensors_status_controllers(self, area: str, controller: str, payload: dict = None, qos: int = 1,
                                       wait_for_publish: bool = False) -> None:
        topic = topics.TOPIC_AREA_SENSORS_STATUS_CONTROLLER.format(
            area=area,
            controller=controller
        )

        self.messages_client.pub(
            topic=topic,
            payload=json.dumps(payload),
            qos=qos,
            wait_for_publish=wait_for_publish
        )

    # SUB METHODS
    def sub_sensors_status_controllers(self, callback, qos: int = 1) -> None:
        topic = topics.TOPIC_AREA_SENSORS_STATUS_CONTROLLER.format(
            area="+",
            controller="+"
        )

        self.messages_client.sub(
            topic=topic,
            funcion=callback,
            qos=qos
        )
