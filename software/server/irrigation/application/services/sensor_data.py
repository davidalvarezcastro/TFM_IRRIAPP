

import typing
from settings import db_mongo_settings
from exceptions.database import ExceptionDatabase
from repositories.mongo.database import MongoManager
from repositories.mongo.dal.sensor_data import SensorDataDAL
from domain.models.sensor_data_historic import QuerySensorData, SensorData


class ServiceSensorsHistoric():
    """ Busines logic for sensor data (historic meteo data)
    """

    def insert(self, data: SensorData) -> typing.Tuple[str, ExceptionDatabase]:
        return SensorDataDAL(
            mongo=MongoManager(collection=db_mongo_settings.COLLECTION_SENSORS)
        ).insert(data=data)

    def get(self, query: QuerySensorData) -> typing.List[SensorData]:
        return SensorDataDAL(
            mongo=MongoManager(collection=db_mongo_settings.COLLECTION_SENSORS)
        ).get(query=query)

    def get_last(self, query: QuerySensorData) -> SensorData:
        return SensorDataDAL(
            mongo=MongoManager(collection=db_mongo_settings.COLLECTION_SENSORS)
        ).get_last(query=query)
