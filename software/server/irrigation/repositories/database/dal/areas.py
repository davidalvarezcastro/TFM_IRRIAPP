import typing

from .interface_areas import InterfaceAreasDAL
from domain.models.areas import Area
from exceptions.database import ExceptionDatabase
from repositories.errors import DUPLICATED, GENERAL_ERROR, NOT_FOUND
from repositories.database.models import AreasORM
from repositories.database.database import session_scope


class AreasDAL(InterfaceAreasDAL):

    @staticmethod
    def init_from_orm_to_model(result: AreasORM) -> Area:
        return Area(
            id=result.id,
            type=result.type,
            name=result.name,
            description=result.description,
            visible=result.visible,
            date=result.date
        )

    @staticmethod
    def insert(area: Area) -> typing.Tuple[int, ExceptionDatabase]:
        with session_scope() as session:
            aux = session.query(AreasORM).filter_by(id=area.id).first()
            if aux is not None:
                raise ExceptionDatabase(type=DUPLICATED, msg=f"Area {area.id} duplicated!")

            area_db = AreasORM(
                name=area.name,
                description=area.description,
                visible=area.visible
            )

            if area.id != -1:
                area_db.id = area.id

            try:
                area_db.add(session)
                return area_db.id
            except Exception as e:
                raise ExceptionDatabase(type=GENERAL_ERROR, msg=str(e))

    @staticmethod
    def update(area: Area) -> ExceptionDatabase:
        with session_scope() as session:
            area_db = session.query(AreasORM).filter_by(id=area.id).first()

            if area_db is None:
                raise ExceptionDatabase(type=NOT_FOUND, msg=f"Area {area.id} is not saved!")

            # only some fields area allowed to be changed
            area_db.name = area.name
            area_db.description = area.description
            area_db.visible = area.visible

            try:
                area_db.update(session)
            except Exception as e:
                raise ExceptionDatabase(type=GENERAL_ERROR, msg=str(e))

    @staticmethod
    def delete(area: Area) -> ExceptionDatabase:
        with session_scope() as session:
            area_db = session.query(AreasORM).filter_by(id=area.id).first()

            try:
                area_db.delete(session)
            except Exception as e:
                raise ExceptionDatabase(type=GENERAL_ERROR, msg=str(e))

    @staticmethod
    def get_by_id(area: int, all_visibility: bool = False) -> Area:
        try:
            query = {
                'id': area
            }
            if not all_visibility:
                query['visible'] = True

            with session_scope() as session:
                result = session.query(AreasORM).filter_by(**query).first()

                if result is None:
                    return None

                return AreasDAL.init_from_orm_to_model(result=result)
        except Exception:
            return None

    @staticmethod
    def get_all(all_visibility: bool = False) -> typing.List[Area]:
        result = []
        query = {}  # all data

        try:
            with session_scope() as session:
                if not all_visibility:
                    query['visible'] = True

                resultDB = session.query(AreasORM).filter_by(**query).all()

                for el in resultDB:
                    result.append(
                        AreasDAL.init_from_orm_to_model(result=el)
                    )
        except Exception:
            pass

        return result
