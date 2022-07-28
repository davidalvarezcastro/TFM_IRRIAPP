
from abc import ABC, abstractmethod

from exceptions.general import NotImplementedError
from domain.models.irrigation_actuator_algorithm import IrrigationActivateActuator


class InterfaceActuatorIrirgationHandler(ABC):

    @staticmethod
    @abstractmethod
    def check_activate_irrigation(query: IrrigationActivateActuator) -> bool:
        raise NotImplementedError
