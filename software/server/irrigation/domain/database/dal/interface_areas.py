import typing
from abc import ABC, abstractmethod

from domain.models.areas import Area
from domain.exceptions.general import NotImplementedError
from domain.exceptions.database import ExceptionDatabase


class InterfaceAreasDAL(ABC):

    @abstractmethod
    def insert(area: Area) -> ExceptionDatabase:
        raise NotImplementedError

    @abstractmethod
    def update(area: Area) -> ExceptionDatabase:
        raise NotImplementedError

    @abstractmethod
    def delete(area: Area) -> ExceptionDatabase:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(area: int, all_visibility: bool = False) -> Area:
        raise NotImplementedError

    @abstractmethod
    def get_all(all_visibility: bool = False) -> typing.List[Area]:
        raise NotImplementedError
