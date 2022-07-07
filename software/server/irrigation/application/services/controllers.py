

import typing
from domain.models.controllers import Controller
from repositories.database.dal.controllers import ControllersDAL
from exceptions.database import ExceptionDatabase


class ServiceControllers():
    """ Busines logic for controllers
    """

    def insert(self, controller: Controller) -> typing.Tuple[int, ExceptionDatabase]:
        return ControllersDAL.insert(controller=controller)

    def update(self, controller: Controller) -> ExceptionDatabase:
        ControllersDAL.update(controller=controller)

    def delete(self, controller: Controller) -> ExceptionDatabase:
        ControllersDAL.delete(controller=controller)

    def get_by_id(self, controller: int, all_visibility: bool = False) -> Controller:
        return ControllersDAL.get_by_id(controller=controller, all_visibility=all_visibility)

    def get_all(self, all_visibility: bool = False) -> typing.List[Controller]:
        return ControllersDAL.get_all(all_visibility=all_visibility)
