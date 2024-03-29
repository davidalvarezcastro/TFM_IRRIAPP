
import typing
import attr
import pymongo

from utils import logger_error
from settings import db_mongo_settings


@attr.s
class MongoManager:
    collection: str = attr.ib()

    def __attrs_post_init__(self):
        client = pymongo.MongoClient(db_mongo_settings.URI)
        db = client[db_mongo_settings.DATABASE]
        col = db[self.collection]

        self.connection = {'connection': client, 'db': db, 'col': col}

    def find(self, query: dict) -> typing.List[typing.Any]:
        """Wrapper for mongodb find (helps with testing)
        """
        return self.connection['col'].find(query)

    def find_last(self, query: dict) -> typing.List[typing.Any]:
        """Wrapper for mongodb find last element inserted into the collection (helps with testing)
        """
        return self.connection['col'].find(query).limit(1).sort([('$natural', -1)])

    def closeMongoConnection(self) -> None:
        try:
            if self.connection is not None and self.connection.get('connection') is not None:
                self.connection['connection'].close()
        except Exception as error:
            logger_error('manager_mongo, closeMongoConnection', error)
