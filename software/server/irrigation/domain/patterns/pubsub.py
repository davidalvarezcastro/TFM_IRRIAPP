# -*- coding: utf-8 -*-
"""Archivo con las definiciones de los patrones utilizados
"""
from abc import ABC, abstractmethod
import attr


@attr.s
class EventoPubSub:
    """ Clase que define los eventos de comunicación en el patrón Observer """
    tipo: str = attr.ib()
    datos: dict = attr.ib()


class Sub(ABC):
    """
    Interfaz de un Observer (subscriptor)
    """

    @abstractmethod
    def update(self, evento: EventoPubSub) -> None:
        """
        Recibe las actualizaciones del estado

        Args:
            evento (EventoPubSub): evento de comunicación indicando el cambio de estado
        """
        pass


class Pub(ABC):
    """
    Interfaz de un Observer (publicador)
    """

    @abstractmethod
    def attach(self, observer: Sub) -> None:
        """ Función para añadir un observer

        Args:
            observer (Sub): observador
        """
        pass

    @abstractmethod
    def detach(self, observer: Sub) -> None:
        """ Función para eliminar un observer

        Args:
            observer (Sub): observador
        """
        pass

    @abstractmethod
    def notify(self, evento: EventoPubSub) -> None:
        """
        Notifica a todos los observers sobre un evento

        Args:
            evento (EventoPubSub): evento de comunicación indicando el cambio de estado
        """
        pass
