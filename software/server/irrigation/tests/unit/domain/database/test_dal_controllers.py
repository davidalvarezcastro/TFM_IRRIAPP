# -*- coding: utf-8 -*-
"""
    areas dal tests
"""
import datetime
import json
import os
import time
import unittest

from unittest.mock import Mock, patch

from domain.exceptions.database import ExceptionDatabase
from domain.models.controllers import Controller
from domain.database.models import ControllersORM
from domain.database.dal.controllers import ControllersDAL


os.environ['MODE'] = "test"


@unittest.skipUnless(os.getenv('UNIT_TESTS'), 'UNIT TEST')
class DALControllersUnitTest(unittest.TestCase):

    print('DALControllersUnitTest...')

    def setUp(self):
        self.id = 1
        self.area = 1
        self.name = "name"
        self.description = "this is a dummy description"
        self.key = "secret"
        self.visible = True

        self.dal = ControllersDAL

        self.controller = Controller(
            id=self.id,
            area=self.area,
            description=self.description,
            key=self.key,
            name=self.name,
            visible=self.visible,
        )

        self.controller_db = ControllersORM(
            id=self.id,
            area=self.area,
            description=self.description,
            key=self.key,
            name=self.name,
            visible=self.visible,
        )

    # INNER METHODS

    # TESTS
    @patch.object(ControllersORM, 'add', return_value=True)
    @patch('domain.database.models.ControllersORM.query')
    def test_insert_call_add_db_function_ok(self, mockFilter, mock):
        mockFilter.filter_by.return_value.first.return_value = None

        self.dal.insert(
            controller=self.controller
        )

        mock.assert_called_once()

    @patch.object(ControllersORM, 'add')
    @patch('domain.database.models.ControllersORM.query')
    def test_insert_call_add_db_function_raise_exception_ok(self, mockFilter, mock):
        mock.side_effect = Mock(
            side_effect=Exception('error'))
        mockFilter.filter_by.return_value.first.return_value = None

        with self.assertRaises(ExceptionDatabase) as context:
            self.dal.insert(
                controller=self.controller
            )

        self.assertTrue("error" in str(context.exception))
        mock.assert_called_once()

    @patch.object(ControllersORM, 'add', return_value=True)
    @patch('domain.database.models.ControllersORM.query')
    def test_insert_raise_exception_duplicated_type_ok(self, mockFilter, mock):
        mockFilter.filter_by.return_value.first.return_value = self.controller_db

        with self.assertRaises(ExceptionDatabase) as context:
            self.dal.insert(
                controller=self.controller
            )

        self.assertTrue(f"Controller {self.controller.id} duplicated!" in str(context.exception))

        mock.assert_not_called()

    @patch.object(ControllersORM, 'update', return_value=True)
    @patch('domain.database.models.ControllersORM.query')
    def test_update_call_update_db_function_ok(self, mockFilter, mock):
        mockFilter.filter_by.return_value.first.return_value = self.controller_db

        self.dal.update(
            controller=self.controller
        )

        mock.assert_called_once()

    @patch.object(ControllersORM, 'update')
    @patch('domain.database.models.ControllersORM.query')
    def test_update_call_update_db_function_raise_exception_ok(self, mockFilter, mock):
        mock.side_effect = Mock(
            side_effect=Exception('error'))
        mockFilter.filter_by.return_value.first.return_value = self.controller_db

        with self.assertRaises(ExceptionDatabase) as context:
            self.dal.update(
                controller=self.controller
            )

        self.assertTrue("error" in str(context.exception))
        mock.assert_called_once()

    @patch.object(ControllersORM, 'add', return_value=True)
    @patch('domain.database.models.ControllersORM.query')
    def test_update_raise_exception_no_type_saved_ok(self, mockFilter, mock):
        mockFilter.filter_by.return_value.first.return_value = None

        with self.assertRaises(ExceptionDatabase) as context:
            self.dal.update(
                controller=self.controller
            )

        self.assertTrue(f"Controller {self.controller.id} is not saved!" in str(context.exception))

        mock.assert_not_called()

    @patch.object(ControllersORM, 'delete', return_value=True)
    @patch('domain.database.models.ControllersORM.query')
    def test_delete_call_delete_db_function_ok(self, mockFilter, mock):
        mockFilter.filter_by.return_value.first.return_value = self.controller_db

        self.dal.delete(
            controller=self.controller
        )

        mock.assert_called_once()

    @patch.object(ControllersORM, 'delete')
    @patch('domain.database.models.ControllersORM.query')
    def test_delete_call_detele_db_function_raise_exception_ok(self, mockFilter, mock):
        mock.side_effect = Mock(
            side_effect=Exception('error'))
        mockFilter.filter_by.return_value.first.return_value = None

        with self.assertRaises(ExceptionDatabase) as context:
            self.dal.delete(
                controller=self.controller
            )

        self.assertTrue("error" in str(context.exception))
        mock.assert_not_called()

    @patch.object(ControllersDAL, 'init_from_orm_to_model')
    @patch('domain.database.models.ControllersORM.query')
    def test_get_id_call_format_inner_function_ok(self, mockFilter, mock):
        mockFilter.filter_by.return_value.first.return_value = self.controller_db

        self.dal.get_by_id(
            controller=self.id
        )

        mock.assert_called_once()

    @patch.object(ControllersDAL, 'init_from_orm_to_model')
    @patch('domain.database.models.ControllersORM.query')
    def test_get_id_returns_none_ok(self, mockFilter, mock):
        mockFilter.filter_by.return_value.first.return_value = None

        result = self.dal.get_by_id(
            controller=self.id
        )

        self.assertIsNone(result)
        mock.assert_not_called()

    @patch('domain.database.models.ControllersORM.query')
    def test_get_all_returns_array_ok(self, mockFilter):
        mockFilter.filter_by.return_value.all.return_value = [self.controller_db]

        result = self.dal.get_all()
        expected = [
            Controller(
                id=self.controller_db.id,
                area=self.controller_db.area,
                name=self.controller_db.name,
                description=self.controller_db.description,
                key=self.controller_db.key,
                visible=self.controller_db.visible,
                date=self.controller_db.date
            )
        ]

        self.assertEqual(result, expected)

    @patch('domain.database.models.ControllersORM.query')
    def test_get_all_returns_empty_array_ok(self, mockFilter):
        mockFilter.filter_by.return_value.all.return_value = []

        result = self.dal.get_all()

        self.assertTrue(len(result) == 0)


if __name__ == '__main__':
    unittest.main()
