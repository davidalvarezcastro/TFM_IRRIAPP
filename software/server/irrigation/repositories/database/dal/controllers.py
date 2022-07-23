import typing

from repositories.errors import DUPLICATED, GENERAL_ERROR, NOT_FOUND
from exceptions.database import ExceptionDatabase
from .interface_controllers import InterfaceControllersDAL
from domain.models.controllers import Controller
from repositories.database.models import ControllersORM
from repositories.database.database import session_scope


class ControllersDAL(InterfaceControllersDAL):

    @staticmethod
    def init_from_orm_to_model(result: ControllersORM) -> Controller:
        return Controller(
            id=result.id,
            area=result.area,
            name=result.name,
            description=result.description,
            key=result.key,
            visible=result.visible,
            date=result.date
        )

    @staticmethod
    def insert(controller: Controller) -> typing.Tuple[int, ExceptionDatabase]:
        with session_scope() as session:
            aux = session.query(ControllersORM).filter_by(id=controller.id).first()
            if aux is not None:
                raise ExceptionDatabase(type=DUPLICATED, msg=f"Controller {controller.id} duplicated!")

            controller_db = ControllersORM(
                area=controller.area,
                name=controller.name,
                description=controller.description,
                key=controller.key,
                visible=controller.visible
            )

            if controller.id != -1:
                controller_db.id = controller.id

            try:
                controller_db.add(session)
                return controller_db.id
            except Exception as e:
                raise ExceptionDatabase(type=GENERAL_ERROR, msg=str(e))

    @staticmethod
    def update(controller: Controller) -> ExceptionDatabase:
        with session_scope() as session:
            controller_db = session.query(ControllersORM).filter_by(id=controller.id).first()

            if controller_db is None:
                raise ExceptionDatabase(type=NOT_FOUND, msg=f"Controller {controller.id} is not saved!")

            # only some fields controllers allowed to be changed
            controller_db.name = controller.name
            controller_db.description = controller.description
            controller_db.key = controller.key
            controller_db.visible = controller.visible

            try:
                controller_db.update(session)
            except Exception as e:
                raise ExceptionDatabase(type=GENERAL_ERROR, msg=str(e))

    @staticmethod
    def delete(controller: Controller) -> ExceptionDatabase:
        with session_scope() as session:
            controller_db = session.query(ControllersORM).filter_by(id=controller.id).first()

            try:
                controller_db.delete(session)
            except Exception as e:
                raise ExceptionDatabase(type=GENERAL_ERROR, msg=str(e))

    @staticmethod
    def get_by_id(controller: int, all_visibility: bool = False) -> Controller:
        try:
            query = {
                'id': controller
            }
            if not all_visibility:
                query['visible'] = True

            with session_scope() as session:
                result = session.query(ControllersORM).filter_by(**query).first()

                if result is None:
                    return None

                return ControllersDAL.init_from_orm_to_model(result=result)
        except Exception:
            return None

    @staticmethod
    def get_all(all_visibility: bool = False) -> typing.List[Controller]:
        result = []
        query = {}  # all data

        try:
            with session_scope() as session:
                if not all_visibility:
                    query['visible'] = True

                resultDB = session.query(ControllersORM).filter_by(**query).all()

                for el in resultDB:
                    result.append(
                        ControllersDAL.init_from_orm_to_model(result=el)
                    )
        except Exception:
            pass

        return result
