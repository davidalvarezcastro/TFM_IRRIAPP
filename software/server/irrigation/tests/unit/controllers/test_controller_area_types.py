# -*- coding: utf-8 -*-
"""
    area types controller tests
"""
import os
import unittest

from unittest.mock import Mock, patch

from controllers.area_types import ControllerAreaTypes
from domain.models.area_types import AreaType
from domain.database.dal.area_types import AreaTypesDAL


os.environ['MODE'] = "test"


@unittest.skipUnless(os.getenv('UNIT_TESTS'), 'UNIT TEST')
class ControllerTypesUnitTest(unittest.TestCase):

    print('ControllerTypesUnitTest...')

    def setUp(self):
        self.id = 1
        self.description = "this is a dummy description"

        self.controller = ControllerAreaTypes()

        self.type = AreaType(
            id=self.id,
            description=self.description,
        )

    # INNER METHODS

    # TESTS
    @patch.object(AreaTypesDAL, 'insert', return_value=True)
    def test_controller_insert_call_dal_insert_ok(self, mock):
        self.controller.insert(
            type=self.type
        )

        mock.assert_called_once()

    @patch.object(AreaTypesDAL, 'insert')
    def test_controller_insert_raise_exception_ok(self, mock):
        mock.side_effect = Mock(
            side_effect=Exception('error'))

        with self.assertRaises(Exception) as context:
            self.controller.insert(
                type=self.type
            )

        self.assertTrue("error" in str(context.exception))
        mock.assert_called_once()

    @patch.object(AreaTypesDAL, 'update', return_value=True)
    def test_controller_update_call_dal_insert_ok(self, mock):
        self.controller.update(
            type=self.type
        )

        mock.assert_called_once()

    @patch.object(AreaTypesDAL, 'update')
    def test_controller_update_raise_exception_ok(self, mock):
        mock.side_effect = Mock(
            side_effect=Exception('error'))

        with self.assertRaises(Exception) as context:
            self.controller.update(
                type=self.type
            )

        self.assertTrue("error" in str(context.exception))
        mock.assert_called_once()

    @patch.object(AreaTypesDAL, 'delete', return_value=True)
    def test_controller_delete_call_dal_insert_ok(self, mock):
        self.controller.delete(
            type=self.type
        )

        mock.assert_called_once()

    @patch.object(AreaTypesDAL, 'delete')
    def test_controller_delete_raise_exception_ok(self, mock):
        mock.side_effect = Mock(
            side_effect=Exception('error'))

        with self.assertRaises(Exception) as context:
            self.controller.delete(
                type=self.type
            )

        self.assertTrue("error" in str(context.exception))
        mock.assert_called_once()

    @patch.object(AreaTypesDAL, 'get_by_id')
    def test_controller_get_id_call_dal_get_id_ok(self, mock):
        self.controller.get_by_id(
            type=self.id
        )

        mock.assert_called_once()

    @patch.object(AreaTypesDAL, 'get_all')
    def test_controller_get_all_call_dal_get_all_ok(self, mock):
        self.controller.get_all()

        mock.assert_called_once()


if __name__ == '__main__':
    unittest.main()
