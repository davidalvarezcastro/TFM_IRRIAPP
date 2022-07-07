# -*- coding: utf-8 -*-
"""Tests para api de incidencia
"""
import attr
import http
import json
import os
import unittest

from unittest.mock import Mock, patch

from api.api import app
from api.settings import API_AREA_TYPES, API_GET_ALL_AREA_TYPES, API_PREFIX, MIMETYPE_JSON
from api.dto.area_type import ApiAreaTypesSchema
from domain.models.area_types import AreaType
from tests.integration.api.test_api_base import ApiBaseIntegrationTest
from application.services.area_types import ServiceAreaTypes


os.environ['MODE'] = "test"


@unittest.skipUnless(os.getenv('INTEGRATION_TESTS'), 'INTEGRATION TEST')
class ApiAreaTypesIntegrationTest(ApiBaseIntegrationTest):

    print('ApiAreaTypesIntegrationTest...')

    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    # INNER METHODS

    # TESTS
    @patch.object(ServiceAreaTypes, 'insert')
    def test_api_post_type_return_created_and_new_type_ok(self, mock):
        post = {
            "description": "test"
        }
        expected_type = 15
        expected = {
            "type": expected_type,
            "msg": f"Type {expected_type} created"
        }
        mock.return_value = expected_type

        result = self.client.post(
            f'{API_PREFIX}{API_AREA_TYPES}',
            data=json.dumps(post),
            content_type=MIMETYPE_JSON
        )
        self.assert_response_201_OK(result)
        data = json.loads(result.data)['data']
        self.assertEqual(data, expected)

    @patch.object(ServiceAreaTypes, 'insert')
    def test_api_post_type_return_bad_request_ok(self, mock):
        post = {
            "asd": "test"
        }
        expected_type = 15
        expected = "Invalid request format data"
        mock.return_value = expected_type

        result = self.client.post(
            f'{API_PREFIX}{API_AREA_TYPES}',
            data=json.dumps(post),
            content_type=MIMETYPE_JSON
        )
        self.assert_response_400_OK(result)
        data = json.loads(result.data)['message']
        self.assertEqual(data, expected)

    @patch.object(ServiceAreaTypes, 'insert')
    def test_api_post_type_return_error_function_insert_ok(self, mock):
        post = {
            "description": "test"
        }
        expected = 'error'
        mock.side_effect = Mock(
            side_effect=Exception(expected))

        result = self.client.post(
            f'{API_PREFIX}{API_AREA_TYPES}',
            data=json.dumps(post),
            content_type=MIMETYPE_JSON
        )
        self.assert_response_500_OK(result)
        data = json.loads(result.data)['message']
        self.assertEqual(data, expected)

    @patch.object(ServiceAreaTypes, 'get_by_id')
    @patch.object(ServiceAreaTypes, 'update', return_value=True)
    def test_api_put_type_return_created_and_new_type_ok(self, mock, mockFilter):
        post = {
            "description": "test"
        }
        type = 10
        expected = {
            "msg": f"Type {type} updated"
        }

        mockFilter.return_value = AreaType(
            id=type,
            description="old"
        )

        result = self.client.put(
            f'{API_PREFIX}{API_AREA_TYPES}/{type}',
            data=json.dumps(post),
            content_type=MIMETYPE_JSON
        )
        self.assert_response_200_OK(result)
        data = json.loads(result.data)['data']
        self.assertEqual(data, expected)

    @patch.object(ServiceAreaTypes, 'update', return_value=True)
    def test_api_put_type_return_bad_request_ok(self, mock):
        post = {
            "asd": "test"
        }
        type = 10
        expected = "Invalid request format data"

        result = self.client.put(
            f'{API_PREFIX}{API_AREA_TYPES}/{type}',
            data=json.dumps(post),
            content_type=MIMETYPE_JSON
        )
        self.assert_response_400_OK(result)
        data = json.loads(result.data)['message']
        self.assertEqual(data, expected)

    @patch.object(ServiceAreaTypes, 'get_by_id')
    @patch.object(ServiceAreaTypes, 'update', return_value=True,)
    def test_api_put_type_return_error_function_update_ok(self, mock, mockFilter):
        post = {
            "description": "test"
        }
        type = 10
        expected = 'error'
        mock.side_effect = Mock(
            side_effect=Exception(expected))

        mockFilter.return_value = AreaType(
            id=type,
            description="old"
        )

        result = self.client.put(
            f'{API_PREFIX}{API_AREA_TYPES}/{type}',
            data=json.dumps(post),
            content_type=MIMETYPE_JSON
        )
        self.assert_response_500_OK(result)
        data = json.loads(result.data)['message']
        self.assertEqual(data, expected)

    @patch.object(ServiceAreaTypes, 'get_by_id')
    @patch.object(ServiceAreaTypes, 'update', return_value=True,)
    def test_api_put_type_return_error_not_found_type_ok(self, mock, mockFilter):
        post = {
            "description": "test"
        }
        type = 10
        expected = f"Type {type} not found"
        mock.side_effect = Mock(
            side_effect=Exception('error'))

        mockFilter.return_value = None

        result = self.client.put(
            f'{API_PREFIX}{API_AREA_TYPES}/{type}',
            data=json.dumps(post),
            content_type=MIMETYPE_JSON
        )
        self.assert_response_404_OK(result)
        data = json.loads(result.data)['message']
        self.assertEqual(data, expected)

    @patch.object(ServiceAreaTypes, 'get_by_id')
    @patch.object(ServiceAreaTypes, 'delete', return_value=True)
    def test_api_delete_type_remove_element_ok(self, mock, mockFilter):
        post = {
            "description": "test"
        }
        type = 10
        expected = {
            "msg": f"Type {type} deleted"
        }

        mockFilter.return_value = AreaType(
            id=type,
            description="old"
        )

        result = self.client.delete(
            f'{API_PREFIX}{API_AREA_TYPES}/{type}',
            data=json.dumps(post),
            content_type=MIMETYPE_JSON
        )
        self.assert_response_200_OK(result)
        data = json.loads(result.data)['data']
        self.assertEqual(data, expected)

    @patch.object(ServiceAreaTypes, 'get_by_id')
    @patch.object(ServiceAreaTypes, 'delete', return_value=True,)
    def test_api_delete_type_return_error_function_delete_ok(self, mock, mockFilter):
        post = {
            "description": "test"
        }
        type = 10
        expected = 'error'
        mock.side_effect = Mock(
            side_effect=Exception(expected))

        mockFilter.return_value = AreaType(
            id=type,
            description="old"
        )

        result = self.client.delete(
            f'{API_PREFIX}{API_AREA_TYPES}/{type}',
            data=json.dumps(post),
            content_type=MIMETYPE_JSON
        )
        self.assert_response_500_OK(result)
        data = json.loads(result.data)['message']
        self.assertEqual(data, expected)

    @patch.object(ServiceAreaTypes, 'get_by_id')
    @patch.object(ServiceAreaTypes, 'delete', return_value=True,)
    def test_api_delete_type_return_error_not_found_type_ok(self, mock, mockFilter):
        post = {
            "description": "test"
        }
        type = 10
        expected = f"Type {type} not found"
        mock.side_effect = Mock(
            side_effect=Exception('error'))

        mockFilter.return_value = None

        result = self.client.delete(
            f'{API_PREFIX}{API_AREA_TYPES}/{type}',
            data=json.dumps(post),
            content_type=MIMETYPE_JSON
        )
        self.assert_response_404_OK(result)
        data = json.loads(result.data)['message']
        self.assertEqual(data, expected)

    @patch.object(ServiceAreaTypes, 'get_by_id')
    def test_api_get_by_id_type_return_type_ok(self, mock):
        type = 10
        expected = AreaType(
            id=type,
            description="old"
        )

        mock.return_value = expected

        result = self.client.get(f'{API_PREFIX}{API_AREA_TYPES}/{type}')
        self.assert_response_200_OK(result)
        data = json.loads(result.data)['data']
        self.assertEqual(data, ApiAreaTypesSchema().dump(expected))

    @patch.object(ServiceAreaTypes, 'get_by_id')
    def test_api_get_by_id_type_return_error_not_found_type_ok(self, mock):
        type = 10
        expected = f"Type {type} not found"

        mock.return_value = None

        result = self.client.get(f'{API_PREFIX}{API_AREA_TYPES}/{type}')
        self.assert_response_404_OK(result)
        data = json.loads(result.data)['message']
        self.assertEqual(data, expected)

    @patch.object(ServiceAreaTypes, 'get_by_id')
    def test_api_get_by_id_type_return_error_function_filter_type_ok(self, mock):
        type = 10
        expected = "error"
        mock.side_effect = Mock(
            side_effect=Exception(expected))

        result = self.client.get(f'{API_PREFIX}{API_AREA_TYPES}/{type}')
        self.assert_response_500_OK(result)
        data = json.loads(result.data)['message']
        self.assertEqual(data, expected)

    @patch.object(ServiceAreaTypes, 'get_all')
    def test_api_get_all_type_return_array_ok(self, mock):
        expected = [
            AreaType(
                id=10,
                description="old"
            ),
            AreaType(
                id=1,
                description="old"
            ),
        ]

        mock.return_value = expected

        result = self.client.get(f'{API_PREFIX}{API_GET_ALL_AREA_TYPES}')
        self.assert_response_200_OK(result)
        data = json.loads(result.data)['data']
        self.assertEqual(data, {'types': ApiAreaTypesSchema(many=True).dump(expected)})

    @patch.object(ServiceAreaTypes, 'get_all')
    def test_api_get_all_type_return_empty_array_ok(self, mock):
        expected = []
        mock.return_value = expected

        result = self.client.get(f'{API_PREFIX}{API_GET_ALL_AREA_TYPES}')
        self.assert_response_200_OK(result)
        data = json.loads(result.data)['data']
        self.assertEqual(data, {'types': expected})

    @patch.object(ServiceAreaTypes, 'get_all')
    def test_api_get_all_type_return_error_function_filter_type_ok(self, mock):
        expected = "error"
        mock.side_effect = Mock(
            side_effect=Exception(expected))

        result = self.client.get(f'{API_PREFIX}{API_GET_ALL_AREA_TYPES}')
        self.assert_response_500_OK(result)
        data = json.loads(result.data)['message']
        self.assertEqual(data, expected)


if __name__ == '__main__':
    unittest.main()
