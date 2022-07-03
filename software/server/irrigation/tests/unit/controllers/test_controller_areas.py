# -*- coding: utf-8 -*-
"""
    areas controller tests
"""
import os
import unittest

from unittest.mock import Mock, patch

from controllers.areas import ControllerAreas
from domain.models.areas import Area
from domain.database.dal.areas import AreasDAL


os.environ['MODE'] = "test"


@unittest.skipUnless(os.getenv('UNIT_TESTS'), 'UNIT TEST')
class ControllerAreasUnitTest(unittest.TestCase):

    print('ControllerAreasUnitTest...')

    def setUp(self):
        self.id = 1
        self.name = "name"
        self.description = "this is a dummy description"
        self.visible = True

        self.controller = ControllerAreas()

        self.area = Area(
            id=self.id,
            description=self.description,
            name=self.name,
            visible=self.visible,
        )

    # INNER METHODS

    # TESTS
    @patch.object(AreasDAL, 'insert', return_value=True)
    def test_controller_insert_call_dal_insert_ok(self, mock):
        self.controller.insert(
            area=self.area
        )

        mock.assert_called_once()

    @patch.object(AreasDAL, 'insert')
    def test_controller_insert_raise_exception_ok(self, mock):
        mock.side_effect = Mock(
            side_effect=Exception('error'))

        with self.assertRaises(Exception) as context:
            self.controller.insert(
                area=self.area
            )

        self.assertTrue("error" in str(context.exception))
        mock.assert_called_once()

    @patch.object(AreasDAL, 'update', return_value=True)
    def test_controller_update_call_dal_insert_ok(self, mock):
        self.controller.update(
            area=self.area
        )

        mock.assert_called_once()

    @patch.object(AreasDAL, 'update')
    def test_controller_update_raise_exception_ok(self, mock):
        mock.side_effect = Mock(
            side_effect=Exception('error'))

        with self.assertRaises(Exception) as context:
            self.controller.update(
                area=self.area
            )

        self.assertTrue("error" in str(context.exception))
        mock.assert_called_once()

    @patch.object(AreasDAL, 'delete', return_value=True)
    def test_controller_delete_call_dal_insert_ok(self, mock):
        self.controller.delete(
            area=self.area
        )

        mock.assert_called_once()

    @patch.object(AreasDAL, 'delete')
    def test_controller_delete_raise_exception_ok(self, mock):
        mock.side_effect = Mock(
            side_effect=Exception('error'))

        with self.assertRaises(Exception) as context:
            self.controller.delete(
                area=self.area
            )

        self.assertTrue("error" in str(context.exception))
        mock.assert_called_once()

    @patch.object(AreasDAL, 'get_by_id')
    def test_controller_get_id_call_dal_get_id_ok(self, mock):
        self.controller.get_by_id(
            area=self.id
        )

        mock.assert_called_once()

    @patch.object(AreasDAL, 'get_all')
    def test_controller_get_all_call_dal_get_all_ok(self, mock):
        self.controller.get_all()

        mock.assert_called_once()


if __name__ == '__main__':
    unittest.main()
