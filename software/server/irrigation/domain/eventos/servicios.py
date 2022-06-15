# coding=utf-8
"""
    Interfaz de comunicación al servidor de eventos
"""
from xmlrpc.client import boolean
import attr
import json
from abc import ABC, abstractmethod

from . import topics as topics
from domain.eventos.wrapper import WrapperEventos


class InterfazEventos(ABC):
    """
    Interfaz de comunicación con el servidor de eventos del sistema
    """

    @abstractmethod
    def pub_estado_sensores_controladores(self, zona: str, controlador: str,
                                          payload: dict = None, qos: int = 1, wait_for_publish: bool = False) -> None:
        """
        Función para emitir el evento de estado de los sensores de un controlador

        Args:
            zona (str): identificador de la zona a la que pertenece el controlador
            controlador (str): identificador del controlador
            payload (dict): listado de los valores leidos por los sensores
            qos (int): calidad del servicio
            wait_for_publish (bool): espera a recibir la confirmación
        Raise:
            Exception
        """
        raise Exception("NotImplementedException")

    @abstractmethod
    def sub_estado_sensores_controladores(self, callback, qos: int = 1) -> None:
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
class ServiciosEventos(InterfazEventos):
    """ Servicio de comunicación para el envío de datos al servidor de eventos del sistema
    """
    cliente_eventos: WrapperEventos = attr.ib()

    # PUB METHODS
    def pub_estado_sensores_controladores(self, zona: str, controlador: str, payload: dict = None, qos: int = 1,
                                          wait_for_publish: bool = False) -> None:
        topic = topics.TOPIC_ZONA_ESTADO_SENSORES_CONTROLADOR.format(
            zona=zona,
            controlador=controlador
        )

        self.cliente_eventos.pub(
            topic=topic,
            payload=json.dumps(payload),
            qos=qos,
            wait_for_publish=wait_for_publish
        )

    # SUB METHODS
    def sub_estado_sensores_controladores(self, callback, qos: int = 1) -> None:
        topic = topics.TOPIC_ZONA_ESTADO_SENSORES_CONTROLADOR.format(
            zona="+",
            controlador="+"
        )

        self.cliente_eventos.sub(
            topic=topic,
            funcion=callback,
            qos=qos
        )
