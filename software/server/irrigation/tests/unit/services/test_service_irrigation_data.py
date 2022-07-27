# -*- coding: utf-8 -*-
"""
    sensor data service tests
"""
import datetime
import mongomock
import os
import unittest

from unittest.mock import Mock, patch

from settings import db_mongo_settings
from application.services.irrigation_data import ServiceIrrigationHistoric
from domain.models.irrigation_data import IrrigationData, QueryIrrigationData
from repositories.mongo.dal.irrigation_data import IrrigationDataDAL


os.environ['MODE'] = "test"


@unittest.skipUnless(os.getenv('UNIT_TESTS'), 'UNIT TEST')
class ServiceIrrigationDataUnitTest(unittest.TestCase):

    print('ServiceIrrigationDataUnitTest...')

    def setUp(self):
        self.controller = ServiceIrrigationHistoric()

        self.irrigation_data = IrrigationData(
            area_id=1,
            area="area1",
            irrigation=0,
            start_date=datetime.datetime(2022, 7, 8, 21, 52, 54, 0),
            end_date=''
        )

        self.query_irrigation_data = QueryIrrigationData(
            area_id=234,
            start_date=datetime.datetime(2022, 7, 2, 21, 00, 00, 0),
            end_date=datetime.datetime(2022, 7, 7, 21, 00, 00, 0),
        )

    # INNER METHODS

    # TESTS
    @patch.object(IrrigationDataDAL, 'insert', return_value=True)
    @mongomock.patch(servers=((db_mongo_settings.HOST, db_mongo_settings.PORT),))
    def test_irrigation_data_historic_insert_call_dal_insert_ok(self, mock):
        self.controller.insert(
            data=self.irrigation_data
        )

        mock.assert_called_once_with(
            data=self.irrigation_data
        )

    @patch.object(IrrigationDataDAL, 'insert')
    @mongomock.patch(servers=((db_mongo_settings.HOST, db_mongo_settings.PORT),))
    def test_irrigation_data_historic_insert_raise_exception_ok(self, mock):
        mock.side_effect = Mock(
            side_effect=Exception('error'))

        with self.assertRaises(Exception) as context:
            self.controller.insert(
                data=self.irrigation_data
            )

        self.assertTrue("error" in str(context.exception))
        mock.assert_called_once()

    @patch.object(IrrigationDataDAL, 'end_irrigation', return_value=True)
    @mongomock.patch(servers=((db_mongo_settings.HOST, db_mongo_settings.PORT),))
    def test_irrigation_data_historic_end_irrigation_call_dal_end_ok(self, mock):
        self.controller.end_irrigation(
            area=self.irrigation_data.area_id
        )

        mock.assert_called_once_with(
            area=self.irrigation_data.area_id
        )

    @patch.object(IrrigationDataDAL, 'get')
    @mongomock.patch(servers=((db_mongo_settings.HOST, db_mongo_settings.PORT),))
    def test_irrigation_data_historic_get_call_dal_get_ok(self, mock):
        self.controller.get(
            query=self.query_irrigation_data
        )

        mock.assert_called_once_with(
            query=self.query_irrigation_data
        )


if __name__ == '__main__':
    unittest.main()
