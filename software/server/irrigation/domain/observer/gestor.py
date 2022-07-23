# coding=utf-8
"""
    Archivo con el servicio de gestión de eventos (publisher)
"""
import attr
import sys
import typing

from . import topics as topics
from utils import logger_error
from domain.patterns import Pub, Sub, EventoPubSub
from domain.eventos.servicios import InterfazEventos


@attr.s
class GestorEventos(Pub):
    """ Control/Gestión de los diferentes eventos
    """
    queue: typing.Any = attr.ib()  # cola para gestionar excepciones
    servicio_eventos: InterfazEventos = attr.ib()  # interfaz de comunicación
    _observers: typing.List[Sub] = attr.ib(default=attr.Factory(list))

    # POST INIT HOOK
    def __attrs_post_init__(self):
        pass

    # PATTERN METHODS
    def attach(self, observer: Sub) -> None:
        """ Función para añadir un observer

        Args:
            observer (Sub): observador
        """
        self._observers.append(observer)

    def detach(self, observer: Sub) -> None:
        """ Función para eliminar un observer

        Args:
            observer (Sub): observador
        """
        self._observers.remove(observer)

    def notify(self, evento: EventoPubSub) -> None:
        """
        Notifica a todos los observers sobre un evento

        Args:
            evento (EventoPubSub): evento de comunicación indicando el cambio de estado
        """
        for observer in self._observers:
            observer.update(evento)

    # METHODS
    def __gestionar_estado_controlador(self, cliente, userdata: dict, mensaje) -> None:
        """Función para gestionar el nuevo estado de los sensores del controlador.

        Args:
            cliente (paho.mqtt.client.Client): información del cliente que recibe el mensaje
            userdata (dict): información del cliente (None si no hay)
            mensaje (paho.mqtt.client.MQTTMessage): información del mensaje (payload, topic, qos)
        """
        try:
            self.notify(evento=EventoPubSub(
                tipo=topics.ESTADO_CONTROLADOR,
                datos={
                    'topic': mensaje.topic,
                    'payload': mensaje.payload
                }
            ))
        except Exception as error:
            self.queue.put(sys.exc_info())
            logger_error(
                nombre="__gestionar_estado_controlador",
                error=error
            )

    def iniciar_subscriptores(self) -> None:
        """ Función que permite iniciar los subscriptores del controlador de eventos
        """
        self.servicio_eventos.sub_estado_sensores_controladores(
            callback=self.__gestionar_estado_controlador)
