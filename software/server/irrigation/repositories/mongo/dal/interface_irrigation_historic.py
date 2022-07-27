from abc import ABC, abstractmethod
import typing

from exceptions.general import NotImplementedError
from exceptions.database import ExceptionDatabase
from domain.models.actuator import QueryActuatorData
from domain.models.irrigation_data import IrrigationData


class InterfaceIrrigationHistoricDAL(ABC):

    @abstractmethod
    def insert(data: IrrigationData) -> typing.Tuple[str, ExceptionDatabase]:
        raise NotImplementedError

    @abstractmethod
    def end_irrigation(area: int) -> ExceptionDatabase:
        raise NotImplementedError

    @abstractmethod
    def get(query: QueryActuatorData) -> typing.List[IrrigationData]:
        raise NotImplementedError
