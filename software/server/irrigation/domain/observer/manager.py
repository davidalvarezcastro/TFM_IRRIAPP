# coding=utf-8
import attr
import sys
import typing

from . import topics as topics
from utils import logger_error
from domain.patterns import Pub, Sub, PubSubEvent
from domain.messages.services import MessagesInterface


@attr.s
class EventsManager(Pub):
    """ Control/Gestión de los diferentes eventos
    """
    queue: typing.Any = attr.ib()
    messages_service: MessagesInterface = attr.ib()
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

    def notify(self, event: PubSubEvent) -> None:
        """
        Notifica a todos los observers sobre un evento

        Args:
            event (PubSubEvent): evento de comunicación indicando el cambio de estado
        """
        for observer in self._observers:
            observer.update(event)

    # METHODS
    def __manage_controller_state(self, client, userdata: dict, mensaje) -> None:
        """Función para gestionar el nuevo estado de los sensores del controlador.

        Args:
            client (paho.mqtt.client.Client): información del cliente que recibe el mensaje
            userdata (dict): información del cliente (None si no hay)
            mensaje (paho.mqtt.client.MQTTMessage): información del mensaje (payload, topic, qos)
        """
        try:
            self.notify(event=PubSubEvent(
                type == topics.CONTROLLER_STATE,
                data={
                    'topic': mensaje.topic,
                    'payload': mensaje.payload
                }
            ))
        except Exception as error:
            self.queue.put(sys.exc_info())
            logger_error(
                nombre="__manage_controller_state",
                error=error
            )

    def init_subs(self) -> None:
        """ Función que permite iniciar los subscriptores del controlador de eventos
        """
        self.messages_service.sub_sensors_state_controllers(
            callback=self.__manage_controller_state)
