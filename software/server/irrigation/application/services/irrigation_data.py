

import typing
from settings import db_mongo_settings
from exceptions.database import ExceptionDatabase
from repositories.mongo.database import MongoManager
from repositories.mongo.dal.irrigation_data import IrrigationDataDAL
from domain.models.irrigation_data import IrrigationData, QueryIrrigationData


class ServiceIrrigationHistoric():
    """ Busines logic for irrigation data
    """

    def insert(self, data: IrrigationData) -> typing.Tuple[str, ExceptionDatabase]:
        return IrrigationDataDAL(
            mongo=MongoManager(collection=db_mongo_settings.COLLECTION_ACTUATOR_IRRIGATION)
        ).insert(data=data)

    def end_irrigation(self, area: int) -> typing.Tuple[str, ExceptionDatabase]:
        return IrrigationDataDAL(
            mongo=MongoManager(collection=db_mongo_settings.COLLECTION_ACTUATOR_IRRIGATION)
        ).end_irrigation(area=area)

    def get(self, query: QueryIrrigationData) -> typing.List[IrrigationData]:
        return IrrigationDataDAL(
            mongo=MongoManager(collection=db_mongo_settings.COLLECTION_ACTUATOR_IRRIGATION)
        ).get(query=query)
