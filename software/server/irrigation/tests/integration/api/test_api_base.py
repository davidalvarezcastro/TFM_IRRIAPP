# -*- coding: utf-8 -*-
"""Base class for api testing
"""
import http
import json
import os
import unittest


from api.settings import MIMETYPE_JSON


os.environ['MODE'] = "test"


@unittest.skipUnless(os.getenv('INTEGRATION_TESTS'), 'INTEGRATION TEST')
class ApiBaseIntegrationTest(unittest.TestCase):
    def assert_OK(self, http_response):
        self.assertEqual(http_response.mimetype, MIMETYPE_JSON)
        aux = json.loads(http_response.data)
        status = aux['status']
        self.assertEqual(status, "success")

    def assert_NOK(self, http_response):
        self.assertEqual(http_response.mimetype, MIMETYPE_JSON)
        aux = json.loads(http_response.data)
        status = aux['status']
        self.assertEqual(status, "error")

    def assert_response_200_OK(self, http_response):
        self.assertEqual(http_response.status_code, http.HTTPStatus.OK)
        self.assert_OK(http_response)

    def assert_response_201_OK(self, http_response):
        self.assertEqual(http_response.status_code, http.HTTPStatus.CREATED)
        self.assert_OK(http_response)

    def assert_response_500_OK(self, http_response):
        self.assertEqual(http_response.status_code, http.HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assert_NOK(http_response)

    def assert_response_400_OK(self, http_response):
        self.assertEqual(http_response.status_code, http.HTTPStatus.BAD_REQUEST)
        self.assert_NOK(http_response)

    def assert_response_404_OK(self, http_response):
        self.assertEqual(http_response.status_code, http.HTTPStatus.NOT_FOUND)
        self.assert_NOK(http_response)


if __name__ == '__main__':
    unittest.main()
