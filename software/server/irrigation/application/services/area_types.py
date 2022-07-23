

import typing
from domain.models.area_types import AreaType
from repositories.database.dal.area_types import AreaTypesDAL
from exceptions.database import ExceptionDatabase


class ServiceAreaTypes():
    """ Busines logic for area types
    """

    def insert(self, type: AreaType) -> typing.Tuple[int, ExceptionDatabase]:
        return AreaTypesDAL.insert(type=type)

    def update(self, type: AreaType) -> ExceptionDatabase:
        AreaTypesDAL.update(type=type)

    def delete(self, type: AreaType) -> ExceptionDatabase:
        AreaTypesDAL.delete(type=type)

    def get_by_id(self, type: int) -> AreaType:
        return AreaTypesDAL.get_by_id(type=type)

    def get_all(self) -> typing.List[AreaType]:
        return AreaTypesDAL.get_all()
