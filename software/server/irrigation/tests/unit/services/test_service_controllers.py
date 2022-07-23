# -*- coding: utf-8 -*-
"""
    controllers controller tests
"""
import os
import unittest

from unittest.mock import Mock, patch

from application.services.controllers import ServiceControllers
from domain.models.controllers import Controller
from repositories.database.dal.controllers import ControllersDAL


os.environ['MODE'] = "test"


@unittest.skipUnless(os.getenv('UNIT_TESTS'), 'UNIT TEST')
class ServiceControllersUnitTest(unittest.TestCase):

    print('ServiceControllersUnitTest...')

    def setUp(self):
        self.id = 1
        self.area = 1
        self.name = "name"
        self.description = "this is a dummy description"
        self.key = "secret"
        self.visible = True

        self.controller = ServiceControllers()

        self.controllerC = Controller(
            id=self.id,
            area=self.area,
            description=self.description,
            key=self.key,
            name=self.name,
            visible=self.visible,
        )

    # INNER METHODS

    # TESTS
    @patch.object(ControllersDAL, 'insert', return_value=True)
    def test_controller_insert_call_dal_insert_ok(self, mock):
        self.controller.insert(
            controller=self.controllerC
        )

        mock.assert_called_once()

    @patch.object(ControllersDAL, 'insert')
    def test_controller_insert_raise_exception_ok(self, mock):
        mock.side_effect = Mock(
            side_effect=Exception('error'))

        with self.assertRaises(Exception) as context:
            self.controller.insert(
                controller=self.controllerC
            )

        self.assertTrue("error" in str(context.exception))
        mock.assert_called_once()

    @patch.object(ControllersDAL, 'update', return_value=True)
    def test_controller_update_call_dal_insert_ok(self, mock):
        self.controller.update(
            controller=self.controllerC
        )

        mock.assert_called_once()

    @patch.object(ControllersDAL, 'update')
    def test_controller_update_raise_exception_ok(self, mock):
        mock.side_effect = Mock(
            side_effect=Exception('error'))

        with self.assertRaises(Exception) as context:
            self.controller.update(
                controller=self.controllerC
            )

        self.assertTrue("error" in str(context.exception))
        mock.assert_called_once()

    @patch.object(ControllersDAL, 'delete', return_value=True)
    def test_controller_delete_call_dal_insert_ok(self, mock):
        self.controller.delete(
            controller=self.controllerC
        )

        mock.assert_called_once()

    @patch.object(ControllersDAL, 'delete')
    def test_controller_delete_raise_exception_ok(self, mock):
        mock.side_effect = Mock(
            side_effect=Exception('error'))

        with self.assertRaises(Exception) as context:
            self.controller.delete(
                controller=self.controllerC
            )

        self.assertTrue("error" in str(context.exception))
        mock.assert_called_once()

    @patch.object(ControllersDAL, 'get_by_id')
    def test_controller_get_id_call_dal_get_id_ok(self, mock):
        self.controller.get_by_id(
            controller=self.id
        )

        mock.assert_called_once()

    @patch.object(ControllersDAL, 'get_all')
    def test_controller_get_all_call_dal_get_all_ok(self, mock):
        self.controller.get_all()

        mock.assert_called_once()


if __name__ == '__main__':
    unittest.main()
