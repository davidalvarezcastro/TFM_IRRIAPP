import typing
from abc import ABC, abstractmethod

from domain.models.controllers import Controller
from exceptions.general import NotImplementedError
from exceptions.database import ExceptionDatabase


class InterfaceControllersDAL(ABC):

    @abstractmethod
    def insert(controller: Controller) -> ExceptionDatabase:
        raise NotImplementedError

    @abstractmethod
    def update(controller: Controller) -> ExceptionDatabase:
        raise NotImplementedError

    @abstractmethod
    def delete(controller: Controller) -> ExceptionDatabase:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(controller: int, all_visibility: bool = False) -> Controller:
        raise NotImplementedError

    @abstractmethod
    def get_all(all_visibility: bool = False) -> typing.List[Controller]:
        raise NotImplementedError
