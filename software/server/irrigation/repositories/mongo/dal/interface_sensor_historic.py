from abc import ABC, abstractmethod
import typing

from exceptions.general import NotImplementedError
from exceptions.database import ExceptionDatabase
from domain.models.sensor_data_historic import SensorData, QuerySensorData


class InterfaceSensorsHistoricDAL(ABC):

    @abstractmethod
    def insert(data: SensorData) -> typing.Tuple[str, ExceptionDatabase]:
        raise NotImplementedError

    @abstractmethod
    def get(query: QuerySensorData) -> typing.List[SensorData]:
        raise NotImplementedError
