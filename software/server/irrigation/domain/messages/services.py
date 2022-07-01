# coding=utf-8
import attr
import json
from abc import ABC, abstractmethod

from . import topics as topics
from domain.messages.wrapper import MessagesClientWrapper


class MessagesInterface(ABC):
    """
    Interfaz de comunicación con el servicio de eventos de la aplicación
    """

    @abstractmethod
    def pub_sensors_state_controllers(self, area: str, controller: str,
                                      payload: dict = None, qos: int = 1, wait_for_publish: bool = False) -> None:
        """
        Función para emitir el evento de estado de los sensores de un controlador

        Args:
            area (str): identificador de la zona a la que pertenece el controlador
            controller (str): identificador del controlador
            payload (dict): listado de los valores leidos por los sensores
            qos (int): calidad del servicio
            wait_for_publish (bool): espera a recibir la confirmación
        Raise:
            Exception
        """
        raise Exception("NotImplementedException")

    @abstractmethod
    def sub_sensors_state_controllers(self, callback, qos: int = 1) -> None:
        """
        Función para subscribirse al evento con los datos de los sensores de los controladores

        Args:
            callback (Function): función para gestionar la recepción de eventos
            qos (int): calidad del servicio
        Raise:
            Exception
        """
        raise Exception("NotImplementedException")


@attr.s
class MessagesServices(MessagesInterface):
    messages_client: MessagesClientWrapper = attr.ib()

    # PUB METHODS
    def pub_sensors_state_controllers(self, area: str, controller: str, payload: dict = None, qos: int = 1,
                                      wait_for_publish: bool = False) -> None:
        topic = topics.TOPIC_AREA_SENSORS_STATE_CONTROLLER.format(
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
    def sub_sensors_state_controllers(self, callback, qos: int = 1) -> None:
        topic = topics.TOPIC_AREA_SENSORS_STATE_CONTROLLER.format(
            area="+",
            controller="+"
        )

        self.messages_client.sub(
            topic=topic,
            funcion=callback,
            qos=qos
        )
