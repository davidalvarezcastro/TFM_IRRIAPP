# -*- coding: utf-8 -*-
"""Archivo con las definiciones de los patrones utilizados
"""
from abc import ABC, abstractmethod
import attr


@attr.s
class PubSubEvent:
    """ Clase que define los eventos de comunicación en el patrón Observer """
    type: str = attr.ib()
    data: dict = attr.ib()


class Sub(ABC):
    """
    Interfaz de un Observer (subscriptor)
    """

    @abstractmethod
    def update(self, event: PubSubEvent) -> None:
        """
        Recibe las actualizaciones del estado

        Args:
            event (PubSubEvent): evento de comunicación indicando el cambio de estado
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
    def notify(self, event: PubSubEvent) -> None:
        """
        Notifica a todos los observers sobre un evento

        Args:
            event (PubSubEvent): evento de comunicación indicando el cambio de estado
        """
        pass
