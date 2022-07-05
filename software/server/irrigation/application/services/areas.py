

import typing
from domain.models.areas import Area
from repositories.database.dal.areas import AreasDAL
from exceptions.database import ExceptionDatabase


class ServiceAreas():
    """ Busines logic for areas
    """

    def insert(self, area: Area) -> ExceptionDatabase:
        AreasDAL.insert(area=area)

    def update(self, area: Area) -> ExceptionDatabase:
        AreasDAL.update(area=area)

    def delete(self, area: Area) -> ExceptionDatabase:
        AreasDAL.delete(area=area)

    def get_by_id(self, area: int, all_visibility: bool = False) -> Area:
        return AreasDAL.get_by_id(area=area, all_visibility=all_visibility)

    def get_all(self, all_visibility: bool = False) -> typing.List[Area]:
        return AreasDAL.get_all(all_visibility=all_visibility)
