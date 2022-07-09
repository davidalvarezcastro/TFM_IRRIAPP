import typing

from .interface_area_types import InterfaceAreaTypesDAL
from repositories.errors import DUPLICATED, GENERAL_ERROR, NOT_FOUND
from repositories.database.models import TypesORM
from domain.models.area_types import AreaType
from exceptions.database import ExceptionDatabase


class AreaTypesDAL(InterfaceAreaTypesDAL):

    @staticmethod
    def init_from_orm_to_model(result: TypesORM) -> AreaType:
        return AreaType(
            id=result.id,
            description=result.description
        )

    @staticmethod
    def insert(type: AreaType) -> typing.Tuple[int, ExceptionDatabase]:
        aux = TypesORM.query.filter_by(id=type.id).first()
        if aux is not None:
            raise ExceptionDatabase(type=DUPLICATED, msg=f"Type {type.id} duplicated!")

        type_db = TypesORM(
            id=type.id,
            description=type.description
        )

        try:
            type_db.add()
            type_db.refresh()
            return type_db.id
        except Exception as e:
            raise ExceptionDatabase(type=GENERAL_ERROR, msg=str(e))

    @staticmethod
    def update(type: AreaType) -> ExceptionDatabase:
        type_db = TypesORM.query.filter_by(id=type.id).first()

        if type_db is None:
            raise ExceptionDatabase(type=NOT_FOUND, msg=f"Type {type.id} is not saved!")

        # only some fields type allowed to be changed
        type_db.description = type.description

        try:
            type_db.update()
        except Exception as e:
            raise ExceptionDatabase(type=GENERAL_ERROR, msg=str(e))

    @staticmethod
    def delete(type: AreaType) -> ExceptionDatabase:
        type_db = TypesORM.query.filter_by(id=type.id).first()

        try:
            type_db.delete()
        except Exception as e:
            raise ExceptionDatabase(type=GENERAL_ERROR, msg=str(e))

    @staticmethod
    def get_by_id(type: int) -> AreaType:
        result = TypesORM.query.filter_by(id=type).first()

        if result is None:
            return None

        return AreaTypesDAL.init_from_orm_to_model(result=result)

    @staticmethod
    def get_all() -> typing.List[AreaType]:
        result = []
        resultDB = TypesORM.query.filter().all()

        for el in resultDB:
            result.append(
                AreaTypesDAL.init_from_orm_to_model(result=el)
            )

        return result
