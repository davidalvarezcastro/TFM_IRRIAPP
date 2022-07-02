import typing

from .interface_controllers import InterfaceControllersDAL
from domain.database.errors import DUPLICATED, GENERAL_ERROR, NOT_FOUND
from domain.database.models import ControllersORM
from domain.models.controllers import Controller
from domain.exceptions.database import ExceptionDatabase


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
    def insert(controller: Controller) -> ExceptionDatabase:
        aux = ControllersORM.query.filter_by(id=controller.id).first()
        if aux is not None:
            raise ExceptionDatabase(type=DUPLICATED, msg=f"Controller {controller.id} duplicated!")

        controllerDB = ControllersORM(
            id=controller.id,
            area=controller.area,
            name=controller.name,
            description=controller.description,
            key=controller.key,
            visible=controller.visible
        )

        try:
            controllerDB.add()
        except Exception as e:
            raise ExceptionDatabase(type=GENERAL_ERROR, msg=str(e))

    @staticmethod
    def update(controller: Controller) -> ExceptionDatabase:
        controllerDB = ControllersORM.query.filter_by(id=controller.id).first()

        if controllerDB is None:
            raise ExceptionDatabase(type=NOT_FOUND, msg=f"Controller {controller.id} is not saved!")

        # only some fields controllers allowed to be changed
        controllerDB.name = controller.name
        controllerDB.description = controller.description
        controllerDB.key = controller.key
        controllerDB.visible = controller.visible

        try:
            controllerDB.update()
        except Exception as e:
            raise ExceptionDatabase(type=GENERAL_ERROR, msg=str(e))

    @staticmethod
    def delete(controller: Controller) -> ExceptionDatabase:
        controllerDB = ControllersORM.query.filter_by(id=controller.id).first()

        try:
            controllerDB.delete()
        except Exception as e:
            raise ExceptionDatabase(type=GENERAL_ERROR, msg=str(e))

    @staticmethod
    def get_by_id(controller: int, all_visibility: bool = False) -> Controller:
        query = {
            'id': controller
        }
        if not all_visibility:
            query['visible'] = True

        result = ControllersORM.query.filter_by(**query).first()

        if result is None:
            return None

        return ControllersDAL.init_from_orm_to_model(result=result)

    @staticmethod
    def get_all(all_visibility: bool = False) -> typing.List[Controller]:
        result = []
        query = {}  # all data

        if not all_visibility:
            query['visible'] = True

        resultDB = ControllersORM.query.filter_by(**query).all()

        for el in resultDB:
            result.append(
                ControllersDAL.init_from_orm_to_model(result=el)
            )

        return result
