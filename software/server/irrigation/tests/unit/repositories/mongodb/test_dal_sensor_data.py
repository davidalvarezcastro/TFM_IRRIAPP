# -*- coding: utf-8 -*-
"""
    sensor data dal tests
"""
import datetime
import mongomock
import os
import unittest

from unittest.mock import Mock, patch
from utils import get_now
from settings import db_mongo_settings
from exceptions.database import ExceptionDatabase
from domain.models.sensor_data_historic import SensorData, QuerySensorData
from repositories.mongo.dal.sensor_data import SensorDataDAL
from repositories.mongo.database import MongoManager


os.environ['MODE'] = "test"


@unittest.skipUnless(os.getenv('UNIT_TESTS'), 'UNIT TEST')
class DALSensorDataUnitTest(unittest.TestCase):

    print('DALSensorDataUnitTest...')

    @mongomock.patch(servers=((db_mongo_settings.HOST, db_mongo_settings.PORT),))
    def setUp(self):
        self.manager = MongoManager(collection="test")
        self.dao = SensorDataDAL(mongo=self.manager)

        self.sensor_data = SensorData(
            controller_id=1,
            controller="controller1",
            area_id=1,
            area="area1",
            humidity=60,
            raining=0,
            temperature=26.6,
            date=datetime.datetime(2022, 7, 8, 21, 52, 54, 0)
        )

        self.manager.connection['col'].delete_many({})

    # # INNER METHODS

    # # TESTS
    @patch.object(MongoManager, 'closeMongoConnection', return_value=True)
    def test_insert_sensor_data_ok(self, mock):
        result = self.dao.insert(
            data=self.sensor_data
        )

        result = self.manager.connection['col'].find()
        result = list(result)[0]
        # remove _id and check
        del result['_id']

        mock.assert_called_once()
        self.assertEqual(result, self.sensor_data.__dict__())

    @patch.object(MongoManager, 'closeMongoConnection', return_value=True)
    def test_insert_none_raise_exception_ok(self, mock):
        expected = "Database error [database_error] => 'NoneType' object has no attribute '__dict__'"

        with self.assertRaises(ExceptionDatabase) as context:
            result = self.dao.insert(
                data=None
            )

        self.assertTrue(expected in str(context.exception))
        mock.assert_called_once()

    @patch.object(MongoManager, 'closeMongoConnection', return_value=True)
    def test_query_sensor_data_no_dates_only_sensor_data_ok(self, mock):
        array_data = []
        # mock data
        for i in range(4):
            data = {
                'controller_id': 1,
                'controller': f"controller{i}",
                'area_id': 1,
                'area': f"area{i}",
                'humidity': 5 * (i + 1),
                'temperature': 10 * (i + 1),
                'raining': 0,
                'date': datetime.datetime(2022, 7, 8, 21, 52, 54, 0),
            }
            array_data.append(data)
            result = self.manager.connection['col'].insert_one(data)

        result = self.dao.get(
            query=QuerySensorData(
                humidity=5
            )
        )
        result = list(result)[0]
        # remove _id and check
        del array_data[0]['_id']

        mock.assert_called_once()
        self.assertEqual(result.__dict__(), array_data[0])

    @patch.object(MongoManager, 'closeMongoConnection', return_value=True)
    def test_get_last_sensor_data_interval_dates_return_data_ok(self, mock):
        array_data = []
        # mock data
        for i in range(4):
            data = {
                'controller_id': 1,
                'controller': f"controller{i}",
                'area_id': 1,
                'area': f"area{i}",
                'humidity': 5 * (i + 1),
                'temperature': 10 * (i + 1),
                'raining': 0,
                'date': datetime.datetime(2022, 7, 5 + i, 21, 00, 00, 0),
            }
            array_data.append(data)
            result = self.manager.connection['col'].insert_one(data)

        result = self.dao.get_last(
            query=QuerySensorData(
                start_date=datetime.datetime(2022, 7, 2, 21, 00, 00, 0),
                end_date=datetime.datetime(2022, 7, 7, 21, 00, 00, 0),
            )
        )

        # remove _id and check
        del array_data[len(array_data) - 1]['_id']

        mock.assert_called_once()
        self.assertEqual(result.__dict__(), array_data[len(array_data) - 1])

    @patch.object(MongoManager, 'closeMongoConnection', return_value=True)
    def test_query_sensor_data_interval_dates_return_data_ok(self, mock):
        array_data = []
        # mock data
        for i in range(4):
            data = {
                'controller_id': 1,
                'controller': f"controller{i}",
                'area_id': 1,
                'area': f"area{i}",
                'humidity': 5 * (i + 1),
                'temperature': 10 * (i + 1),
                'raining': 0,
                'date': datetime.datetime(2022, 7, 5 + i, 21, 00, 00, 0),
            }
            array_data.append(data)
            result = self.manager.connection['col'].insert_one(data)

        result = self.dao.get(
            query=QuerySensorData(
                start_date=datetime.datetime(2022, 7, 2, 21, 00, 00, 0),
                end_date=datetime.datetime(2022, 7, 7, 21, 00, 00, 0),
            )
        )

        mock.assert_called_once()
        self.assertTrue(len(list(result)) == 3)

    @patch.object(MongoManager, 'closeMongoConnection', return_value=True)
    def test_query_sensor_data_interval_dates_return_no_data_ok(self, mock):
        array_data = []
        # mock data
        for i in range(4):
            data = {
                'controller_id': 1,
                'controller': f"controller{i}",
                'area_id': 1,
                'area': f"area{i}",
                'humidity': 5 * (i + 1),
                'temperature': 10 * (i + 1),
                'raining': 0,
                'date': datetime.datetime(2022, 7, 5 + i, 21, 00, 00, 0),
            }
            array_data.append(data)
            result = self.manager.connection['col'].insert_one(data)

        result = self.dao.get(
            query=QuerySensorData(
                end_date=datetime.datetime(2022, 7, 4, 21, 00, 00, 0),
            )
        )

        mock.assert_called_once()
        self.assertTrue(len(list(result)) == 0)

    @ patch.object(MongoManager, 'closeMongoConnection', return_value=True)
    def test_query_sensor_data_sensor_data_query_ok(self, mock):
        array_data = []
        # mock data
        for i in range(4):
            data = {
                'controller_id': 1,
                'controller': f"controller{i}",
                'area_id': 1,
                'area': f"area{i}",
                'humidity': 5 * (i + 1),
                'temperature': 10 * (i + 1),
                'raining': 0,
                'date': datetime.datetime(2022, 7, 5 + i, 21, 00, 00, 0),
            }
            array_data.append(data)
            result = self.manager.connection['col'].insert_one(data)

        result = self.dao.get(
            query=QuerySensorData(
                end_date=datetime.datetime(2022, 7, 4, 21, 00, 00, 0),
            )
        )

        mock.assert_called_once()
        self.assertTrue(len(list(result)) == 0)

    @ patch.object(MongoManager, 'closeMongoConnection', return_value=True)
    @ patch.object(MongoManager, "find", return_value=[])
    def test_query_none_raise_exception_ok(self, mock_find, mock):
        expected = "Database error [database_error] => 'NoneType' object has no attribute 'get_equal_values'"

        result = self.dao.get(
            query=QuerySensorData(
                controller_id=3,
                humidity=30,
                temperature=39,
                start_date=datetime.datetime(2022, 7, 2, 21, 00, 00, 0),
                end_date=datetime.datetime(2022, 7, 7, 21, 00, 00, 0),
            )
        )

        mock_find.assert_called_once_with(
            query={
                'controller_id': {'$eq': 3},
                'humidity': {'$gte': 30},
                'temperature': {'$gte': 39},
                'date': {
                    '$gte': datetime.datetime(2022, 7, 2, 21, 00, 00, 0),
                    '$lte': datetime.datetime(2022, 7, 7, 21, 00, 00, 0),
                },
            }
        )
        mock.assert_called_once()


if __name__ == '__main__':
    unittest.main()
