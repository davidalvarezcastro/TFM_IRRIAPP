import typing

from .interface_area_types import InterfaceAreaTypesDAL
from domain.database.errors import DUPLICATED, GENERAL_ERROR, NOT_FOUND
from domain.database.models import TypesORM
from domain.models.area_types import AreaType
from domain.exceptions.database import ExceptionDatabase


class AreaTypesDAL(InterfaceAreaTypesDAL):

    @staticmethod
    def init_from_orm_to_model(result: TypesORM) -> AreaType:
        return AreaType(
            id=result.id,
            description=result.description
        )

    @staticmethod
    def insert(type: AreaType) -> ExceptionDatabase:
        aux = TypesORM.query.filter_by(id=type.id).first()
        if aux is not None:
            raise ExceptionDatabase(type=DUPLICATED, msg=f"Type {type.id} duplicated!")

        typeDB = TypesORM(
            id=type.id,
            description=type.description
        )

        try:
            typeDB.add()
        except Exception as e:
            raise ExceptionDatabase(type=GENERAL_ERROR, msg=str(e))

    @staticmethod
    def update(type: AreaType) -> ExceptionDatabase:
        typeDB = TypesORM.query.filter_by(id=type.id).first()

        if typeDB is None:
            raise ExceptionDatabase(type=NOT_FOUND, msg=f"Type {type.id} is not saved!")

        # only some fields type allowed to be changed
        typeDB.description = type.description

        try:
            typeDB.update()
        except Exception as e:
            raise ExceptionDatabase(type=GENERAL_ERROR, msg=str(e))

    @staticmethod
    def delete(type: AreaType) -> ExceptionDatabase:
        typeDB = TypesORM.query.filter_by(id=type.id).first()

        try:
            typeDB.delete()
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
