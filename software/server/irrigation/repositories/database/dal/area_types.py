import typing

from repositories.errors import DUPLICATED, GENERAL_ERROR, NOT_FOUND
from exceptions.database import ExceptionDatabase
from .interface_area_types import InterfaceAreaTypesDAL
from domain.models.area_types import AreaType
from repositories.database.models import TypesORM
from repositories.database.database import session_scope


class AreaTypesDAL(InterfaceAreaTypesDAL):

    @staticmethod
    def init_from_orm_to_model(result: TypesORM) -> AreaType:
        return AreaType(
            id=result.id,
            description=result.description
        )

    @staticmethod
    def insert(type: AreaType) -> typing.Tuple[int, ExceptionDatabase]:
        with session_scope() as session:
            aux = session.query(TypesORM).filter_by(id=type.id).first()
            if aux is not None:
                raise ExceptionDatabase(type=DUPLICATED, msg=f"Type {type.id} duplicated!")

            type_db = TypesORM(
                id=type.id,
                description=type.description
            )

            try:
                type_db.add(session)
                return type_db.id
            except Exception as e:
                raise ExceptionDatabase(type=GENERAL_ERROR, msg=str(e))

    @staticmethod
    def update(type: AreaType) -> ExceptionDatabase:
        with session_scope() as session:
            type_db = session.query(TypesORM).filter_by(id=type.id).first()

            if type_db is None:
                raise ExceptionDatabase(type=NOT_FOUND, msg=f"Type {type.id} is not saved!")

            # only some fields type allowed to be changed
            type_db.description = type.description

            try:
                type_db.update(session)
            except Exception as e:
                raise ExceptionDatabase(type=GENERAL_ERROR, msg=str(e))

    @staticmethod
    def delete(type: AreaType) -> ExceptionDatabase:
        with session_scope() as session:
            type_db = session.query(TypesORM).filter_by(id=type.id).first()

            try:
                type_db.delete(session)
            except Exception as e:
                raise ExceptionDatabase(type=GENERAL_ERROR, msg=str(e))

    @staticmethod
    def get_by_id(type: int) -> AreaType:
        try:
            with session_scope() as session:
                result = session.query(TypesORM).filter_by(id=type).first()

                if result is None:
                    return None

                return AreaTypesDAL.init_from_orm_to_model(result=result)
        except Exception:
            return None

    @staticmethod
    def get_all() -> typing.List[AreaType]:
        result = []

        try:
            with session_scope() as session:
                resultDB = session.query(TypesORM).filter().all()

                for el in resultDB:
                    result.append(
                        AreaTypesDAL.init_from_orm_to_model(result=el)
                    )
        except Exception:
            pass

        return result
