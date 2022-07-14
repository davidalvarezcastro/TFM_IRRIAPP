# -*- coding: utf-8 -*-
"""Areas api tests
"""
import attr
import http
import json
import os
import unittest

from unittest.mock import Mock, patch

from api.api import app
from utils.dates import get_datetime_from_string, get_now
from api.settings import API_GET_HISTORIC_SENSOR_DATA_CONTROLLER, API_PREFIX, MIMETYPE_JSON
from api.dto.sensor_data import ApiSensorDataSchema
from domain.models.sensor_data_historic import QuerySensorData, SensorData
from application.services.sensor_data import ServiceSensorsHistoric
from tests.integration.api.test_api_base import ApiBaseIntegrationTest


os.environ['MODE'] = "test"


@unittest.skipUnless(os.getenv('INTEGRATION_TESTS'), 'INTEGRATION TEST')
class ApiSensorDataIntegrationTest(ApiBaseIntegrationTest):

    print('ApiSensorDataIntegrationTest...')

    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

        self.controller = 1
        self.url_get_filter = API_GET_HISTORIC_SENSOR_DATA_CONTROLLER.format(controller=self.controller)

    # INNER METHODS

    # TESTS
    @patch.object(ServiceSensorsHistoric, 'get')
    def test_api_get_filter_sensor_data_return_array_ok(self, mock):
        expected = [
            SensorData(
                area_id=1,
                controller_id=1,
                area="name",
                controller="name",
                humidity=34,
                temperature=36,
                raining=False,
                date=get_now()
            ),
            SensorData(
                area_id=2,
                controller_id=2,
                area="name",
                controller="name",
                humidity=34,
                temperature=36,
                raining=False,
                date=get_now()
            ),
        ]

        mock.return_value = expected

        result = self.client.get(f'{API_PREFIX}{self.url_get_filter}')
        self.assert_response_200_OK(result)
        data = json.loads(result.data)['data']

        self.assertEqual(data, {'sensor_data': ApiSensorDataSchema(many=True).dump(expected)})

    @patch.object(ServiceSensorsHistoric, 'get')
    def test_api_get_filter_sensor_data_send_right_query_to_service_ok(self, mock):
        expected = []
        mock.return_value = expected

        self.humidity = 66
        self.temperature = 25
        self.raining = True
        self.start_date = "2022-07-13T07:00:00"
        self.end_date = "2022-07-13T23:00:00"

        query_parameters = f"?humidity={self.humidity}&temperature={self.temperature}&raining={self.raining}&start_date={self.start_date}&end_date={self.end_date}"

        result = self.client.get(f'{API_PREFIX}{self.url_get_filter}{query_parameters}')
        self.assert_response_200_OK(result)
        data = json.loads(result.data)['data']

        self.assertEqual(data, {'sensor_data': expected})
        mock.assert_called_once_with(
            query=QuerySensorData(
                controller_id=self.controller,
                humidity=self.humidity,
                temperature=self.temperature,
                raining=self.raining,
                start_date=get_datetime_from_string(self.start_date),
                end_date=get_datetime_from_string(self.end_date),
            )
        )

    @patch.object(ServiceSensorsHistoric, 'get')
    def test_api_get_filter_sensor_data_return_empty_array_ok(self, mock):
        expected = []
        mock.return_value = expected

        result = self.client.get(f'{API_PREFIX}{self.url_get_filter}')
        self.assert_response_200_OK(result)
        data = json.loads(result.data)['data']

        self.assertEqual(data, {'sensor_data': expected})

    @patch.object(ServiceSensorsHistoric, 'get')
    def test_api_get_filter_sensor_data_return_error_function_filter_sensor_data_ok(self, mock):
        expected = "error"
        mock.side_effect = Mock(
            side_effect=Exception(expected))

        result = self.client.get(f'{API_PREFIX}{self.url_get_filter}')
        self.assert_response_500_OK(result)
        data = json.loads(result.data)['message']

        self.assertEqual(data, expected)


if __name__ == '__main__':
    unittest.main()
