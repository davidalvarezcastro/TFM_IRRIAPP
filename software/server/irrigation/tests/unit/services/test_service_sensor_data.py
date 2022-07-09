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
from application.services.sensor_data import ServiceSensorsHistoric
from domain.models.sensor_data_historic import SensorData, QuerySensorData
from repositories.mongo.dal.sensor_data import SensorDataDAL


os.environ['MODE'] = "test"


@unittest.skipUnless(os.getenv('UNIT_TESTS'), 'UNIT TEST')
class ServiceSensorHistoricUnitTest(unittest.TestCase):

    print('ServiceSensorHistoricUnitTest...')

    def setUp(self):
        self.controller = ServiceSensorsHistoric()

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

        self.query_sensor_data = QuerySensorData(
            controller_id=2,
            area_id=234,
            start_date=datetime.datetime(2022, 7, 2, 21, 00, 00, 0),
            end_date=datetime.datetime(2022, 7, 7, 21, 00, 00, 0),
        )

    # INNER METHODS

    # TESTS
    @patch.object(SensorDataDAL, 'insert', return_value=True)
    @mongomock.patch(servers=((db_mongo_settings.HOST, db_mongo_settings.PORT),))
    def test_sensor_data_historic_insert_call_dal_insert_ok(self, mock):
        self.controller.insert(
            data=self.sensor_data
        )

        mock.assert_called_once_with(
            data=self.sensor_data
        )

    @patch.object(SensorDataDAL, 'insert')
    @mongomock.patch(servers=((db_mongo_settings.HOST, db_mongo_settings.PORT),))
    def test_sensor_data_historic_insert_raise_exception_ok(self, mock):
        mock.side_effect = Mock(
            side_effect=Exception('error'))

        with self.assertRaises(Exception) as context:
            self.controller.insert(
                data=self.sensor_data
            )

        print(str(context.exception))
        self.assertTrue("error" in str(context.exception))
        mock.assert_called_once()

    @patch.object(SensorDataDAL, 'get')
    @mongomock.patch(servers=((db_mongo_settings.HOST, db_mongo_settings.PORT),))
    def test_sensor_data_historic_get_call_dal_get_ok(self, mock):
        self.controller.get(
            query=self.query_sensor_data
        )

        mock.assert_called_once_with(
            query=self.query_sensor_data
        )


if __name__ == '__main__':
    unittest.main()
