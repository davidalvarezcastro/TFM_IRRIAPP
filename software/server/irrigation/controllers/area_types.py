

import typing
from domain.models.area_types import AreaType
from domain.database.dal.area_types import AreaTypesDAL
from domain.exceptions.database import ExceptionDatabase


class ControllerAreaTypes():
    """ Busines logic for area types
    """

    def insert(self, type: AreaType) -> ExceptionDatabase:
        AreaTypesDAL.insert(type=type)

    def update(self, type: AreaType) -> ExceptionDatabase:
        AreaTypesDAL.update(type=type)

    def delete(self, type: AreaType) -> ExceptionDatabase:
        AreaTypesDAL.delete(type=type)

    def get_by_id(self, type: int) -> AreaType:
        return AreaTypesDAL.get_by_id(type=type)

    def get_all(self) -> typing.List[AreaType]:
        return AreaTypesDAL.get_all()
