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
from domain.models.irrigation_data import IrrigationData, QueryIrrigationData
from repositories.mongo.dal.irrigation_data import IrrigationDataDAL
from repositories.mongo.database import MongoManager


os.environ['MODE'] = "test"


@unittest.skipUnless(os.getenv('UNIT_TESTS'), 'UNIT TEST')
class DALIrrigationDataUnitTest(unittest.TestCase):

    print('DALIrrigationDataUnitTest...')

    @mongomock.patch(servers=((db_mongo_settings.HOST, db_mongo_settings.PORT),))
    def setUp(self):
        self.manager = MongoManager(collection="test")
        self.dao = IrrigationDataDAL(mongo=self.manager)

        self.irrigation_data = IrrigationData(
            area_id=1,
            area="area1",
            irrigation=1,
            start_date=datetime.datetime(2022, 7, 8, 21, 52, 54, 0),
            end_date=''
        )

        self.manager.connection['col'].delete_many({})

    # # INNER METHODS

    # # TESTS
    @patch.object(MongoManager, 'closeMongoConnection', return_value=True)
    def test_insert_irrigation_data_ok(self, mock):
        result = self.dao.insert(
            data=self.irrigation_data
        )

        result = self.manager.connection['col'].find()
        result = list(result)[0]
        # remove _id and check
        del result['_id']

        mock.assert_called_once()
        self.assertEqual(result, self.irrigation_data.__dict__())

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
    def test_end_irrigation_data_ok(self, mock):
        data = {
            'area_id': 1,
            'area': "area-1",
            'irrigation': 1,
            'start_date': datetime.datetime(2022, 7, 5, 21, 00, 00, 0),
        }
        result = self.manager.connection['col'].insert_one(data)

        self.dao.end_irrigation(
            area=self.irrigation_data.area_id
        )
        result = self.manager.connection['col'].find()

        result = list(result)[0]
        # remove _id and check

        end_date = result['end_date']
        del result['_id']

        mock.assert_called_once()
        self.assertNotEqual(end_date, '')
        self.assertEqual(data['irrigation'], result['irrigation'])

    @patch.object(MongoManager, 'closeMongoConnection', return_value=True)
    def test_query_irrigation_data_no_dates_only_irrigation_data_ok(self, mock):
        array_data = []
        # mock data
        for i in range(4):
            data = {
                'area_id': 1,
                'area': f"area{i}",
                'irrigation': 0 if i % 2 else 1,
                'start_date': datetime.datetime(2022, 7, 8, 21, 52, 54, 0),
                'end_date': ''
            }
            array_data.append(data)
            result = self.manager.connection['col'].insert_one(data)

        result = self.dao.get(
            query=QueryIrrigationData(
                area_id=1,
                irrigation=1
            )
        )
        result = list(result)[0]
        # remove _id and check
        del array_data[0]['_id']

        mock.assert_called_once()
        self.assertEqual(result.__dict__(), array_data[0])

    @patch.object(MongoManager, 'closeMongoConnection', return_value=True)
    def test_query_irrigation_data_not_close_return_data_ok(self, mock):
        array_data = []
        # mock data
        data = {
            'area_id': 1,
            'area': "area1",
            'irrigation': 1,
            'start_date': datetime.datetime(2022, 7, 5, 21, 00, 00, 0),
            'end_date': ''
        }
        result = self.manager.connection['col'].insert_one(data)

        result = self.dao.get(
            query=QueryIrrigationData(
                area_id=1,
                end_date='',
            )
        )

        mock.assert_called_once()
        self.assertTrue(len(list(result)) == 1)

    @patch.object(MongoManager, 'closeMongoConnection', return_value=True)
    def test_query_irrigation_data_interval_dates_return_no_data_ok(self, mock):
        array_data = []
        # mock data
        for i in range(4):
            data = {
                'area_id': 1,
                'area': f"area{i}",
                'irrigation': 0 if i % 2 else 1,
                'start_date': datetime.datetime(2022, 7, 5 + i, 21, 00, 00, 0),
                'end_date': ''
            }
            array_data.append(data)
            result = self.manager.connection['col'].insert_one(data)

        result = self.dao.get(
            query=QueryIrrigationData(
                end_date=datetime.datetime(2022, 7, 4, 21, 00, 00, 0),
            )
        )

        mock.assert_called_once()
        self.assertTrue(len(list(result)) == 0)

    @ patch.object(MongoManager, 'closeMongoConnection', return_value=True)
    def test_query_irrigation_data_irrigation_data_query_ok(self, mock):
        array_data = []
        # mock data
        for i in range(4):
            data = {
                'area_id': 1,
                'area': f"area{i}",
                'irrigation': 0 if i % 2 else 1,
                'start_date': datetime.datetime(2022, 7, 5 + i, 21, 00, 00, 0),
                'end_date': ''
            }
            array_data.append(data)
            result = self.manager.connection['col'].insert_one(data)

        result = self.dao.get(
            query=QueryIrrigationData(
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
            query=QueryIrrigationData(
                area_id=3,
                irrigation=1,
                start_date=datetime.datetime(2022, 7, 2, 21, 00, 00, 0),
                end_date=datetime.datetime(2022, 7, 7, 21, 00, 00, 0),
            )
        )

        mock_find.assert_called_once_with(
            query={
                'area_id': {'$eq': 3},
                'irrigation': {'$eq': 1},
                'start_date': {
                    '$gte': datetime.datetime(2022, 7, 2, 21, 00, 00, 0)
                },
                'end_date': {
                    '$lte': datetime.datetime(2022, 7, 7, 21, 00, 00, 0)
                },
            }
        )
        mock.assert_called_once()


if __name__ == '__main__':
    unittest.main()
