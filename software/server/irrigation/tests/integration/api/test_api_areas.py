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
from api.settings import API_AREA_AREAS, API_GET_ALL_AREAS, API_PREFIX, MIMETYPE_JSON
from api.dto.area import ApiAreasSchema
from domain.models.areas import Area
from tests.integration.api.test_api_base import ApiBaseIntegrationTest
from application.services.areas import ServiceAreas


os.environ['MODE'] = "test"


@unittest.skipUnless(os.getenv('INTEGRATION_TESTS'), 'INTEGRATION TEST')
class ApiAreasIntegrationTest(ApiBaseIntegrationTest):

    print('ApiAreasIntegrationTest...')

    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    # INNER METHODS

    # TESTS
    @patch.object(ServiceAreas, 'insert')
    def test_api_post_area_return_created_and_new_area_ok(self, mock):
        post = {
            "name": "test_name_testing",
            "description": "test",
            "visible": 1
        }
        expected_area = 15
        expected = {
            "area": expected_area,
            "msg": f"Area {post['name']} ({expected_area}) created"
        }
        mock.return_value = expected_area

        result = self.client.post(
            f'{API_PREFIX}{API_AREA_AREAS}',
            data=json.dumps(post),
            content_type=MIMETYPE_JSON
        )
        self.assert_response_201_OK(result)
        data = json.loads(result.data)['data']
        self.assertEqual(data, expected)

    @patch.object(ServiceAreas, 'insert')
    def test_api_post_area_return_bad_request_ok(self, mock):
        post = {
            "name": "test_name_testing",
            "asd": "test",
            "visible": 1
        }
        expected_area = 15
        expected = "Invalid request format data"
        mock.return_value = expected_area

        result = self.client.post(
            f'{API_PREFIX}{API_AREA_AREAS}',
            data=json.dumps(post),
            content_type=MIMETYPE_JSON
        )
        self.assert_response_400_OK(result)
        data = json.loads(result.data)['message']
        self.assertEqual(data, expected)

    @patch.object(ServiceAreas, 'insert')
    def test_api_post_area_return_error_function_insert_ok(self, mock):
        post = {
            "name": "test_name_testing",
            "description": "test",
            "visible": 1
        }
        expected = 'error'
        mock.side_effect = Mock(
            side_effect=Exception(expected))

        result = self.client.post(
            f'{API_PREFIX}{API_AREA_AREAS}',
            data=json.dumps(post),
            content_type=MIMETYPE_JSON
        )
        self.assert_response_500_OK(result)
        data = json.loads(result.data)['message']
        self.assertEqual(data, expected)

    @patch.object(ServiceAreas, 'get_by_id')
    @patch.object(ServiceAreas, 'update', return_value=True)
    def test_api_put_area_return_created_and_new_area_ok(self, mock, mockFilter):
        post = {
            "description": "test",
            "visible": 1
        }
        area = 10
        expected = {
            "msg": f"Area {area} updated"
        }

        mockFilter.return_value = Area(
            id=area,
            name="name1",
            description="old",
            visible=1
        )

        result = self.client.put(
            f'{API_PREFIX}{API_AREA_AREAS}/{area}',
            data=json.dumps(post),
            content_type=MIMETYPE_JSON
        )
        self.assert_response_200_OK(result)
        data = json.loads(result.data)['data']
        self.assertEqual(data, expected)

    @patch.object(ServiceAreas, 'update', return_value=True)
    def test_api_put_area_return_bad_request_ok(self, mock):
        post = {
            "asd": "test",
            "visible": 1
        }
        area = 10
        expected = "Invalid request format data"

        result = self.client.put(
            f'{API_PREFIX}{API_AREA_AREAS}/{area}',
            data=json.dumps(post),
            content_type=MIMETYPE_JSON
        )
        self.assert_response_400_OK(result)
        data = json.loads(result.data)['message']
        self.assertEqual(data, expected)

    @patch.object(ServiceAreas, 'get_by_id')
    @patch.object(ServiceAreas, 'update', return_value=True,)
    def test_api_put_area_return_error_function_update_ok(self, mock, mockFilter):
        post = {
            "description": "test",
            "visible": 1
        }
        area = 10
        expected = 'error'
        mock.side_effect = Mock(
            side_effect=Exception(expected))

        mockFilter.return_value = Area(
            name="name1",
            id=area,
            description="old"
        )

        result = self.client.put(
            f'{API_PREFIX}{API_AREA_AREAS}/{area}',
            data=json.dumps(post),
            content_type=MIMETYPE_JSON
        )
        self.assert_response_500_OK(result)
        data = json.loads(result.data)['message']
        self.assertEqual(data, expected)

    @patch.object(ServiceAreas, 'get_by_id')
    @patch.object(ServiceAreas, 'update', return_value=True,)
    def test_api_put_area_return_error_not_found_area_ok(self, mock, mockFilter):
        post = {
            "description": "test",
            "visible": 1
        }
        area = 10
        expected = f"Area {area} not found"
        mock.side_effect = Mock(
            side_effect=Exception('error'))

        mockFilter.return_value = None

        result = self.client.put(
            f'{API_PREFIX}{API_AREA_AREAS}/{area}',
            data=json.dumps(post),
            content_type=MIMETYPE_JSON
        )
        self.assert_response_404_OK(result)
        data = json.loads(result.data)['message']
        self.assertEqual(data, expected)

    @patch.object(ServiceAreas, 'get_by_id')
    @patch.object(ServiceAreas, 'delete', return_value=True)
    def test_api_delete_area_remove_element_ok(self, mock, mockFilter):
        post = {
            "name": "test_name_testing",
            "description": "test",
            "visible": 1
        }
        area = 10
        expected = {
            "msg": f"Area {area} deleted"
        }

        mockFilter.return_value = Area(
            id=area,
            name="name1",
            description="old",
            visible=1
        )

        result = self.client.delete(
            f'{API_PREFIX}{API_AREA_AREAS}/{area}',
            data=json.dumps(post),
            content_type=MIMETYPE_JSON
        )
        self.assert_response_200_OK(result)
        data = json.loads(result.data)['data']
        self.assertEqual(data, expected)

    @patch.object(ServiceAreas, 'get_by_id')
    @patch.object(ServiceAreas, 'delete', return_value=True)
    def test_api_delete_area_return_not_foundareanot_visible_ok(self, mock, mockFilter):
        post = {
            "name": "test_name_testing",
            "description": "test",
            "visible": 0
        }
        area = 10
        expected = {
            "msg": f"Area {area} deleted"
        }

        mockFilter.return_value = Area(
            id=area,
            name="name1",
            description="old",
            visible=1
        )

        result = self.client.delete(
            f'{API_PREFIX}{API_AREA_AREAS}/{area}',
            data=json.dumps(post),
            content_type=MIMETYPE_JSON
        )
        self.assert_response_200_OK(result)
        data = json.loads(result.data)['data']
        self.assertEqual(data, expected)

    @patch.object(ServiceAreas, 'get_by_id')
    @patch.object(ServiceAreas, 'delete', return_value=True,)
    def test_api_delete_area_return_error_function_delete_ok(self, mock, mockFilter):
        post = {
            "name": "test_name_testing",
            "description": "test",
            "visible": 1
        }
        area = 10
        expected = 'error'
        mock.side_effect = Mock(
            side_effect=Exception(expected))

        mockFilter.return_value = Area(
            id=area,
            name="name1",
            description="old",
            visible=1
        )

        result = self.client.delete(
            f'{API_PREFIX}{API_AREA_AREAS}/{area}',
            data=json.dumps(post),
            content_type=MIMETYPE_JSON
        )
        self.assert_response_500_OK(result)
        data = json.loads(result.data)['message']
        self.assertEqual(data, expected)

    @patch.object(ServiceAreas, 'get_by_id')
    @patch.object(ServiceAreas, 'delete', return_value=True,)
    def test_api_delete_area_return_error_not_found_area_ok(self, mock, mockFilter):
        post = {
            "name": "test_name_testing",
            "description": "test",
            "visible": 1
        }
        area = 10
        expected = f"Area {area} not found"
        mock.side_effect = Mock(
            side_effect=Exception('error'))

        mockFilter.return_value = None

        result = self.client.delete(
            f'{API_PREFIX}{API_AREA_AREAS}/{area}',
            data=json.dumps(post),
            content_type=MIMETYPE_JSON
        )
        self.assert_response_404_OK(result)
        data = json.loads(result.data)['message']
        self.assertEqual(data, expected)

    @patch.object(ServiceAreas, 'get_by_id')
    def test_api_get_by_id_area_return_area_ok(self, mock):
        area = 10
        expected = Area(
            id=area,
            name="name",
            description="old",
            visible=1
        )

        mock.return_value = expected

        result = self.client.get(f'{API_PREFIX}{API_AREA_AREAS}/{area}')
        self.assert_response_200_OK(result)
        data = json.loads(result.data)['data']
        self.assertEqual(data, ApiAreasSchema().dump(expected))

    @patch.object(ServiceAreas, 'get_by_id')
    def test_api_get_by_id_area_return_not_found_area_not_visible_ok(self, mock):
        area = 10
        expected = Area(
            id=area,
            name="name",
            description="old",
            visible=0
        )

        mock.return_value = expected

        result = self.client.get(f'{API_PREFIX}{API_AREA_AREAS}/{area}')
        self.assert_response_200_OK(result)
        data = json.loads(result.data)['data']
        self.assertEqual(data, ApiAreasSchema().dump(expected))

    @patch.object(ServiceAreas, 'get_by_id')
    def test_api_get_by_id_area_return_error_not_found_area_ok(self, mock):
        area = 10
        expected = f"Area {area} not found"

        mock.return_value = None

        result = self.client.get(f'{API_PREFIX}{API_AREA_AREAS}/{area}')
        self.assert_response_404_OK(result)
        data = json.loads(result.data)['message']
        self.assertEqual(data, expected)

    @patch.object(ServiceAreas, 'get_by_id')
    def test_api_get_by_id_area_return_error_function_filter_area_ok(self, mock):
        area = 10
        expected = "error"
        mock.side_effect = Mock(
            side_effect=Exception(expected))

        result = self.client.get(f'{API_PREFIX}{API_AREA_AREAS}/{area}')
        self.assert_response_500_OK(result)
        data = json.loads(result.data)['message']
        self.assertEqual(data, expected)

    @patch.object(ServiceAreas, 'get_all')
    def test_api_get_all_area_return_array_ok(self, mock):
        expected = [
            Area(
                id=10,
                name="name1",
                description="old",
                visible=1
            ),
            Area(
                id=1,
                name="name2",
                description="old",
                visible=1
            ),
        ]

        mock.return_value = expected

        result = self.client.get(f'{API_PREFIX}{API_GET_ALL_AREAS}')
        self.assert_response_200_OK(result)
        data = json.loads(result.data)['data']
        self.assertEqual(data, {'areas': ApiAreasSchema(many=True).dump(expected)})

    @patch.object(ServiceAreas, 'get_all')
    def test_api_get_all_area_return_empty_array_ok(self, mock):
        expected = []
        mock.return_value = expected

        result = self.client.get(f'{API_PREFIX}{API_GET_ALL_AREAS}')
        self.assert_response_200_OK(result)
        data = json.loads(result.data)['data']
        self.assertEqual(data, {'areas': expected})

    @patch.object(ServiceAreas, 'get_all')
    def test_api_get_all_area_return_error_function_filter_area_ok(self, mock):
        expected = "error"
        mock.side_effect = Mock(
            side_effect=Exception(expected))

        result = self.client.get(f'{API_PREFIX}{API_GET_ALL_AREAS}')
        self.assert_response_500_OK(result)
        data = json.loads(result.data)['message']
        self.assertEqual(data, expected)


if __name__ == '__main__':
    unittest.main()
