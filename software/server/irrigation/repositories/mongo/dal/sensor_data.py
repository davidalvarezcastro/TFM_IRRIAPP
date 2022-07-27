import typing
import attr


from .interface_sensor_historic import InterfaceSensorsHistoricDAL
from repositories.errors import DUPLICATED, GENERAL_ERROR
from repositories.mongo.database import MongoManager
from domain.models.sensor_data_historic import SensorData, QuerySensorData
from exceptions.database import ExceptionDatabase


@attr.s
class SensorDataDAL(InterfaceSensorsHistoricDAL):
    mongo: MongoManager = attr.ib()

    def init_from_dict_to_model(self, result: dict) -> SensorData:
        return SensorData(
            controller_id=result.get('controller_id'),
            controller=result.get('controller'),
            area_id=result.get('area_id'),
            area=result.get('area'),
            humidity=result.get('humidity'),
            raining=result.get('raining'),
            temperature=result.get('temperature'),
            date=result.get('date')
        )

    def insert(self, data: SensorData) -> typing.Tuple[str, ExceptionDatabase]:
        try:
            db = self.mongo.connection['col']
            result = db.insert_one(data.__dict__())
            return result.inserted_id
        except Exception as e:
            raise ExceptionDatabase(type=GENERAL_ERROR, msg=str(e))
        finally:
            self.mongo.closeMongoConnection()

    def get(self, query: QuerySensorData) -> typing.List[SensorData]:
        result = []
        query_mongo = {}

        try:
            db = self.mongo

            # parse sensor query
            for value in query.get_equal_values():
                query_mongo[value] = {
                    '$eq': getattr(query, value)
                }
            for value in query.get_greater_equals_than_values():
                query_mongo[value] = {
                    '$gte': getattr(query, value)
                }

            # special treatment for dates
            if query.start_date is not None:
                if 'date' not in query_mongo:
                    query_mongo['date'] = {}

                query_mongo['date']['$gte'] = query.start_date
            if query.end_date is not None:
                if 'date' not in query_mongo:
                    query_mongo['date'] = {}

                query_mongo['date']['$lte'] = query.end_date

            aux = db.find(
                query=query_mongo
            )

            for data in aux:
                result.append(
                    self.init_from_dict_to_model(result=data)
                )
        except Exception as e:
            raise ExceptionDatabase(type=GENERAL_ERROR, msg=str(e))
        finally:
            self.mongo.closeMongoConnection()

        return result

    def get_last(self, query: QuerySensorData) -> SensorData:
        result = []
        query_mongo = {}

        try:
            db = self.mongo

            # parse sensor query
            for value in query.get_equal_values():
                query_mongo[value] = {
                    '$eq': getattr(query, value)
                }
            for value in query.get_greater_equals_than_values():
                query_mongo[value] = {
                    '$gte': getattr(query, value)
                }

            aux = db.find_last(
                query=query_mongo,
            )
            aux = list(aux)

            if len(aux) > 0:
                return self.init_from_dict_to_model(result=aux[0])
            else:
                return None
        except Exception as e:
            raise ExceptionDatabase(type=GENERAL_ERROR, msg=str(e))
        finally:
            self.mongo.closeMongoConnection()

        return result
