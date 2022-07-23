# -*- coding: utf-8 -*-
"""Controllers api tests
"""
import attr
import http
import json
import os
import unittest

from unittest.mock import Mock, patch

from api.api import app
from api.settings import API_AREA_CONTROLLERS, API_GET_ALL_CONTROLLERS, API_PREFIX, MIMETYPE_JSON
from api.dto.controller import ApiControllersSchema
from domain.models.controllers import Controller
from application.services.controllers import ServiceControllers
from tests.integration.api.test_api_base import ApiBaseIntegrationTest


os.environ['MODE'] = "test"


@unittest.skipUnless(os.getenv('INTEGRATION_TESTS'), 'INTEGRATION TEST')
class ApiControllersIntegrationTest(ApiBaseIntegrationTest):

    print('ApiControllersIntegrationTest...')

    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    # INNER METHODS

    # TESTS
    @patch.object(ServiceControllers, 'insert')
    def test_api_post_controller_return_created_and_new_controller_ok(self, mock):
        post = {
            "name": "test_name_testing",
            "description": "test",
            "visible": 1
        }
        expected_controller = 15
        expected = {
            "controller": expected_controller,
            "msg": f"Controller {post['name']} ({expected_controller}) created"
        }
        mock.return_value = expected_controller

        result = self.client.post(
            f'{API_PREFIX}{API_AREA_CONTROLLERS}',
            data=json.dumps(post),
            content_type=MIMETYPE_JSON
        )
        self.assert_response_201_OK(result)
        data = json.loads(result.data)['data']
        self.assertEqual(data, expected)

    @patch.object(ServiceControllers, 'insert')
    def test_api_post_controller_return_bad_request_ok(self, mock):
        post = {
            "name": "test_name_testing",
            "asd": "test",
            "visible": 1
        }
        expected_controller = 15
        expected = "Invalid request format data"
        mock.return_value = expected_controller

        result = self.client.post(
            f'{API_PREFIX}{API_AREA_CONTROLLERS}',
            data=json.dumps(post),
            content_type=MIMETYPE_JSON
        )
        self.assert_response_400_OK(result)
        data = json.loads(result.data)['message']
        self.assertEqual(data, expected)

    @patch.object(ServiceControllers, 'insert')
    def test_api_post_controller_return_error_function_insert_ok(self, mock):
        post = {
            "name": "test_name_testing",
            "description": "test",
            "visible": 1
        }
        expected = 'error'
        mock.side_effect = Mock(
            side_effect=Exception(expected))

        result = self.client.post(
            f'{API_PREFIX}{API_AREA_CONTROLLERS}',
            data=json.dumps(post),
            content_type=MIMETYPE_JSON
        )
        self.assert_response_500_OK(result)
        data = json.loads(result.data)['message']
        self.assertEqual(data, expected)

    @patch.object(ServiceControllers, 'get_by_id')
    @patch.object(ServiceControllers, 'update', return_value=True)
    def test_api_put_controller_return_updated_controller_ok(self, mock, mockFilter):
        post = {
            "description": "test",
            "visible": 1
        }
        controller = 4
        controller = 4
        area = 10
        expected = {
            "msg": f"Controller {controller} updated"
        }

        mockFilter.return_value = Controller(
            id=controller,
            area=area,
            name="name1",
            description="old",
            visible=1
        )

        result = self.client.put(
            f'{API_PREFIX}{API_AREA_CONTROLLERS}/{controller}',
            data=json.dumps(post),
            content_type=MIMETYPE_JSON
        )
        self.assert_response_200_OK(result)
        data = json.loads(result.data)['data']
        self.assertEqual(data, expected)

    @ patch.object(ServiceControllers, 'update', return_value=True)
    def test_api_put_controller_return_bad_request_ok(self, mock):
        post = {
            "asd": "test",
            "visible": 1
        }
        controller = 4
        area = 10
        expected = "Invalid request format data"

        result = self.client.put(
            f'{API_PREFIX}{API_AREA_CONTROLLERS}/{controller}',
            data=json.dumps(post),
            content_type=MIMETYPE_JSON
        )
        self.assert_response_400_OK(result)
        data = json.loads(result.data)['message']
        self.assertEqual(data, expected)

    @ patch.object(ServiceControllers, 'get_by_id')
    @ patch.object(ServiceControllers, 'update', return_value=True,)
    def test_api_put_controller_return_error_function_update_ok(self, mock, mockFilter):
        post = {
            "description": "test",
            "visible": 1
        }
        controller = 4
        area = 10
        expected = 'error'
        mock.side_effect = Mock(
            side_effect=Exception(expected))

        mockFilter.return_value = Controller(
            name="name1",
            area=area,
            id=controller,
            description="old"
        )

        result = self.client.put(
            f'{API_PREFIX}{API_AREA_CONTROLLERS}/{controller}',
            data=json.dumps(post),
            content_type=MIMETYPE_JSON
        )
        self.assert_response_500_OK(result)
        data = json.loads(result.data)['message']
        self.assertEqual(data, expected)

    @ patch.object(ServiceControllers, 'get_by_id')
    @ patch.object(ServiceControllers, 'update', return_value=True,)
    def test_api_put_controller_return_error_not_found_controller_ok(self, mock, mockFilter):
        post = {
            "description": "test",
            "visible": 1
        }
        controller = 4
        area = 10
        expected = f"Controller {controller} not found"
        mock.side_effect = Mock(
            side_effect=Exception('error'))

        mockFilter.return_value = None

        result = self.client.put(
            f'{API_PREFIX}{API_AREA_CONTROLLERS}/{controller}',
            data=json.dumps(post),
            content_type=MIMETYPE_JSON
        )
        self.assert_response_404_OK(result)
        data = json.loads(result.data)['message']
        self.assertEqual(data, expected)

    @ patch.object(ServiceControllers, 'get_by_id')
    @ patch.object(ServiceControllers, 'delete', return_value=True)
    def test_api_delete_controller_remove_element_ok(self, mock, mockFilter):
        post = {
            "name": "test_name_testing",
            "description": "test",
            "visible": 1
        }
        controller = 4
        area = 10
        expected = {
            "msg": f"Controller {controller} deleted"
        }

        mockFilter.return_value = Controller(
            id=controller,
            area=area,
            name="name1",
            description="old",
            visible=1
        )

        result = self.client.delete(
            f'{API_PREFIX}{API_AREA_CONTROLLERS}/{controller}',
            data=json.dumps(post),
            content_type=MIMETYPE_JSON
        )
        self.assert_response_200_OK(result)
        data = json.loads(result.data)['data']
        self.assertEqual(data, expected)

    @ patch.object(ServiceControllers, 'get_by_id')
    @ patch.object(ServiceControllers, 'delete', return_value=True)
    def test_api_delete_controller_return_not_foundareanot_visible_ok(self, mock, mockFilter):
        post = {
            "name": "test_name_testing",
            "description": "test",
            "visible": 0
        }
        controller = 4
        area = 10
        expected = {
            "msg": f"Controller {controller} deleted"
        }

        mockFilter.return_value = Controller(
            id=controller,
            area=area,
            name="name1",
            description="old",
            visible=1
        )

        result = self.client.delete(
            f'{API_PREFIX}{API_AREA_CONTROLLERS}/{controller}',
            data=json.dumps(post),
            content_type=MIMETYPE_JSON
        )
        self.assert_response_200_OK(result)
        data = json.loads(result.data)['data']
        self.assertEqual(data, expected)

    @ patch.object(ServiceControllers, 'get_by_id')
    @ patch.object(ServiceControllers, 'delete', return_value=True,)
    def test_api_delete_controller_return_error_function_delete_ok(self, mock, mockFilter):
        post = {
            "name": "test_name_testing",
            "description": "test",
            "visible": 1
        }
        controller = 4
        area = 10
        expected = 'error'
        mock.side_effect = Mock(
            side_effect=Exception(expected))

        mockFilter.return_value = Controller(
            id=controller,
            area=area,
            name="name1",
            description="old",
            visible=1
        )

        result = self.client.delete(
            f'{API_PREFIX}{API_AREA_CONTROLLERS}/{controller}',
            data=json.dumps(post),
            content_type=MIMETYPE_JSON
        )
        self.assert_response_500_OK(result)
        data = json.loads(result.data)['message']
        self.assertEqual(data, expected)

    @ patch.object(ServiceControllers, 'get_by_id')
    @ patch.object(ServiceControllers, 'delete', return_value=True,)
    def test_api_delete_controller_return_error_not_found_controller_ok(self, mock, mockFilter):
        post = {
            "name": "test_name_testing",
            "description": "test",
            "visible": 1
        }
        controller = 4
        area = 10
        expected = f"Controller {controller} not found"
        mock.side_effect = Mock(
            side_effect=Exception('error'))

        mockFilter.return_value = None

        result = self.client.delete(
            f'{API_PREFIX}{API_AREA_CONTROLLERS}/{controller}',
            data=json.dumps(post),
            content_type=MIMETYPE_JSON
        )
        self.assert_response_404_OK(result)
        data = json.loads(result.data)['message']
        self.assertEqual(data, expected)

    @ patch.object(ServiceControllers, 'get_by_id')
    def test_api_get_by_id_controller_return_controller_ok(self, mock):
        controller = 4
        area = 10
        expected = Controller(
            id=controller,
            area=area,
            name="name",
            description="old",
            visible=1
        )

        mock.return_value = expected

        result = self.client.get(f'{API_PREFIX}{API_AREA_CONTROLLERS}/{controller}')
        self.assert_response_200_OK(result)
        data = json.loads(result.data)['data']
        self.assertEqual(data, ApiControllersSchema().dump(expected))

    @ patch.object(ServiceControllers, 'get_by_id')
    def test_api_get_by_id_controller_return_not_found_controller_not_visible_ok(self, mock):
        controller = 4
        area = 10
        expected = Controller(
            id=controller,
            area=area,
            name="name",
            description="old",
            visible=0
        )

        mock.return_value = expected

        result = self.client.get(f'{API_PREFIX}{API_AREA_CONTROLLERS}/{controller}')
        self.assert_response_200_OK(result)
        data = json.loads(result.data)['data']
        self.assertEqual(data, ApiControllersSchema().dump(expected))

    @ patch.object(ServiceControllers, 'get_by_id')
    def test_api_get_by_id_controller_return_error_not_found_controller_ok(self, mock):
        controller = 4
        area = 10
        expected = f"Controller {controller} not found"

        mock.return_value = None

        result = self.client.get(f'{API_PREFIX}{API_AREA_CONTROLLERS}/{controller}')
        self.assert_response_404_OK(result)
        data = json.loads(result.data)['message']
        self.assertEqual(data, expected)

    @ patch.object(ServiceControllers, 'get_by_id')
    def test_api_get_by_id_controller_return_error_function_filter_controller_ok(self, mock):
        controller = 4
        area = 10
        expected = "error"
        mock.side_effect = Mock(
            side_effect=Exception(expected))

        result = self.client.get(f'{API_PREFIX}{API_AREA_CONTROLLERS}/{controller}')
        self.assert_response_500_OK(result)
        data = json.loads(result.data)['message']
        self.assertEqual(data, expected)

    @ patch.object(ServiceControllers, 'get_all')
    def test_api_get_all_controller_return_array_ok(self, mock):
        expected = [
            Controller(
                id=10,
                area=2,
                name="name1",
                description="old",
                visible=1
            ),
            Controller(
                id=1,
                area=2,
                name="name2",
                description="old",
                visible=1
            ),
        ]

        mock.return_value = expected

        result = self.client.get(f'{API_PREFIX}{API_GET_ALL_CONTROLLERS}')
        self.assert_response_200_OK(result)
        data = json.loads(result.data)['data']
        self.assertEqual(data, {'controllers': ApiControllersSchema(many=True).dump(expected)})

    @ patch.object(ServiceControllers, 'get_all')
    def test_api_get_all_controller_return_empty_array_ok(self, mock):
        expected = []
        mock.return_value = expected

        result = self.client.get(f'{API_PREFIX}{API_GET_ALL_CONTROLLERS}')
        self.assert_response_200_OK(result)
        data = json.loads(result.data)['data']
        self.assertEqual(data, {'controllers': expected})

    @ patch.object(ServiceControllers, 'get_all')
    def test_api_get_all_controller_return_error_function_filter_controller_ok(self, mock):
        expected = "error"
        mock.side_effect = Mock(
            side_effect=Exception(expected))

        result = self.client.get(f'{API_PREFIX}{API_GET_ALL_CONTROLLERS}')
        self.assert_response_500_OK(result)
        data = json.loads(result.data)['message']
        self.assertEqual(data, expected)


if __name__ == '__main__':
    unittest.main()
