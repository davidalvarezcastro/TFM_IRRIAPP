import datetime
import typing
import attr


from .interface_irrigation_historic import InterfaceIrrigationHistoricDAL
from repositories.errors import DUPLICATED, GENERAL_ERROR
from repositories.mongo.database import MongoManager
from domain.models.irrigation_data import IrrigationData, QueryIrrigationData
from exceptions.database import ExceptionDatabase


@attr.s
class IrrigationDataDAL(InterfaceIrrigationHistoricDAL):
    mongo: MongoManager = attr.ib()

    def init_from_dict_to_model(self, result: dict) -> IrrigationData:
        return IrrigationData(
            area_id=result.get('area_id'),
            area=result.get('area'),
            irrigation=result.get('irrigation'),
            start_date=result.get('start_date', ''),
            end_date=result.get('end_date', ''),
        )

    def insert(self, data: IrrigationData) -> typing.Tuple[str, ExceptionDatabase]:
        try:
            db = self.mongo.connection['col']
            result = db.insert_one(data.__dict__())
            return result.inserted_id
        except Exception as e:
            raise ExceptionDatabase(type=GENERAL_ERROR, msg=str(e))
        finally:
            self.mongo.closeMongoConnection()

    def end_irrigation(self, area: int) -> typing.Tuple[str, ExceptionDatabase]:
        try:
            db = self.mongo.connection['col']
            query = {"area_id": {
                "$eq": area
            }}
            update = {"$set": {"end_date": datetime.datetime.now()}}
            result = db.update_one(query, update)
            return area
        except Exception as e:
            raise ExceptionDatabase(type=GENERAL_ERROR, msg=str(e))
        finally:
            self.mongo.closeMongoConnection()

    def get(self, query: QueryIrrigationData) -> typing.List[IrrigationData]:
        result = []
        query_mongo = {}

        try:
            db = self.mongo

            # parse irrigation query
            query_mongo['area_id'] = {
                '$eq': getattr(query, 'area_id')
            }
            query_mongo['irrigation'] = {
                '$eq': getattr(query, 'irrigation')
            }

            # special treatment for dates
            if query.start_date is not None:
                if 'start_date' not in query_mongo:
                    query_mongo['start_date'] = {}

                query_mongo['start_date']['$gte'] = query.start_date
            if query.end_date is not None:
                if 'end_date' not in query_mongo:
                    query_mongo['end_date'] = {}

                if query.end_date != '':
                    query_mongo['end_date']['$lte'] = query.end_date
                else:
                    query_mongo['end_date']['$eq'] = ''

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
