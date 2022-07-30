# -*- coding: utf-8 -*-
"""Areas api tests
"""
from datetime import timedelta
import attr
import http
import json
import os
import unittest

from unittest.mock import Mock, patch

from api.api import app
from utils.dates import get_datetime_from_string, get_now
from api.settings import API_GET_HISTORICAL_ACTUATOR_DATA_AREA, API_PREFIX
from api.dto.actuator import ApiActuatorActivationSchema
from domain.models.irrigation_data import QueryIrrigationData, ActuatorData
from application.services.irrigation_data import ServiceIrrigationHistoric
from tests.integration.api.test_api_base import ApiBaseIntegrationTest


os.environ['MODE'] = "test"


@unittest.skipUnless(os.getenv('INTEGRATION_TESTS'), 'INTEGRATION TEST')
class ApiActuatorDataIntegrationTest(ApiBaseIntegrationTest):

    print('ApiActuatorDataIntegrationTest...')

    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

        self.area = 1
        self.url_get_filter = API_GET_HISTORICAL_ACTUATOR_DATA_AREA.format(area=self.area)

    # INNER METHODS

    # TESTS
    @patch.object(ServiceIrrigationHistoric, 'get')
    def test_api_get_filter_actuator_activation_return_array_ok(self, mock):
        expected = [
            ActuatorData(
                area_id=1,
                area="name",
                start_date=get_now(),
                end_date=get_now() + timedelta(minutes=5)
            ),
            ActuatorData(
                area_id=1,
                area="name",
                start_date=get_now() + timedelta(hours=5),
                end_date=get_now() + timedelta(hours=6)
            ),
        ]

        mock.return_value = expected

        result = self.client.get(f'{API_PREFIX}{self.url_get_filter}')
        self.assert_response_200_OK(result)
        data = json.loads(result.data)['data']

        self.assertEqual(data, {'actuator_activation': ApiActuatorActivationSchema(many=True).dump(expected)})

    @patch.object(ServiceIrrigationHistoric, 'get')
    def test_api_get_filter_actuator_activation_send_right_query_to_service_ok(self, mock):
        expected = []
        mock.return_value = expected

        self.start_date = "2022-07-13T07:00:00"
        self.end_date = "2022-07-13T23:00:00"

        query_parameters = f"?start_date={self.start_date}&end_date={self.end_date}"

        result = self.client.get(f'{API_PREFIX}{self.url_get_filter}{query_parameters}')
        self.assert_response_200_OK(result)
        data = json.loads(result.data)['data']

        self.assertEqual(data, {'actuator_activation': expected})
        mock.assert_called_once_with(
            query=QueryIrrigationData(
                area_id=self.area,
                start_date=get_datetime_from_string(self.start_date),
                end_date=get_datetime_from_string(self.end_date),
            )
        )

    @patch.object(ServiceIrrigationHistoric, 'get')
    def test_api_get_filter_actuator_activation_return_empty_array_ok(self, mock):
        expected = []
        mock.return_value = expected

        result = self.client.get(f'{API_PREFIX}{self.url_get_filter}')
        self.assert_response_200_OK(result)
        data = json.loads(result.data)['data']

        self.assertEqual(data, {'actuator_activation': expected})

    @patch.object(ServiceIrrigationHistoric, 'get')
    def test_api_get_filter_actuator_activation_return_error_function_filter_actuator_activation_ok(
            self, mock):
        expected = "error"
        mock.side_effect = Mock(
            side_effect=Exception(expected))

        result = self.client.get(f'{API_PREFIX}{self.url_get_filter}')
        self.assert_response_500_OK(result)
        data = json.loads(result.data)['message']

        self.assertEqual(data, expected)


if __name__ == '__main__':
    unittest.main()
