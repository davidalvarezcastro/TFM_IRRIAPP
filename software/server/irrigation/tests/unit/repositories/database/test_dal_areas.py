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

from exceptions.database import ExceptionDatabase
from domain.models.areas import Area
from repositories.database.models import AreasORM
from repositories.database.dal.areas import AreasDAL


os.environ['MODE'] = "test"


@unittest.skipUnless(os.getenv('UNIT_TESTS'), 'UNIT TEST')
class DALAreasUnitTest(unittest.TestCase):

    print('DALAreasUnitTest...')

    def setUp(self):
        self.id = 1
        self.name = "name"
        self.description = "this is a dummy description"
        self.visible = True

        self.dal = AreasDAL

        self.area = Area(
            id=self.id,
            description=self.description,
            name=self.name,
            visible=self.visible,
        )

        self.area_db = AreasORM(
            id=self.id,
            description=self.description,
            name=self.name,
            visible=self.visible,
        )

    # INNER METHODS

    # TESTS
    @patch.object(AreasORM, 'add', return_value=True)
    @patch('repositories.database.models.AreasORM.query')
    def test_insert_call_add_db_function_ok(self, mockFilter, mock):
        mockFilter.filter_by.return_value.first.return_value = None

        self.dal.insert(
            area=self.area
        )

        mock.assert_called_once()

    @patch.object(AreasORM, 'add')
    @patch('repositories.database.models.AreasORM.query')
    def test_insert_call_add_db_function_raise_exception_ok(self, mockFilter, mock):
        mock.side_effect = Mock(
            side_effect=Exception('error'))
        mockFilter.filter_by.return_value.first.return_value = None

        with self.assertRaises(ExceptionDatabase) as context:
            self.dal.insert(
                area=self.area
            )

        self.assertTrue("error" in str(context.exception))
        mock.assert_called_once()

    @patch.object(AreasORM, 'add', return_value=True)
    @patch('repositories.database.models.AreasORM.query')
    def test_insert_raise_exception_duplicated_type_ok(self, mockFilter, mock):
        mockFilter.filter_by.return_value.first.return_value = self.area_db

        with self.assertRaises(ExceptionDatabase) as context:
            self.dal.insert(
                area=self.area
            )

        self.assertTrue(f"Area {self.area.id} duplicated!" in str(context.exception))

        mock.assert_not_called()

    @patch.object(AreasORM, 'update', return_value=True)
    @patch('repositories.database.models.AreasORM.query')
    def test_update_call_update_db_function_ok(self, mockFilter, mock):
        mockFilter.filter_by.return_value.first.return_value = self.area_db

        self.dal.update(
            area=self.area
        )

        mock.assert_called_once()

    @patch.object(AreasORM, 'update')
    @patch('repositories.database.models.AreasORM.query')
    def test_update_call_update_db_function_raise_exception_ok(self, mockFilter, mock):
        mock.side_effect = Mock(
            side_effect=Exception('error'))
        mockFilter.filter_by.return_value.first.return_value = self.area_db

        with self.assertRaises(ExceptionDatabase) as context:
            self.dal.update(
                area=self.area
            )

        self.assertTrue("error" in str(context.exception))
        mock.assert_called_once()

    @patch.object(AreasORM, 'add', return_value=True)
    @patch('repositories.database.models.AreasORM.query')
    def test_update_raise_exception_no_type_saved_ok(self, mockFilter, mock):
        mockFilter.filter_by.return_value.first.return_value = None

        with self.assertRaises(ExceptionDatabase) as context:
            self.dal.update(
                area=self.area
            )

        self.assertTrue(f"Area {self.area.id} is not saved!" in str(context.exception))

        mock.assert_not_called()

    @patch.object(AreasORM, 'delete', return_value=True)
    @patch('repositories.database.models.AreasORM.query')
    def test_delete_call_delete_db_function_ok(self, mockFilter, mock):
        mockFilter.filter_by.return_value.first.return_value = self.area_db

        self.dal.delete(
            area=self.area
        )

        mock.assert_called_once()

    @patch.object(AreasORM, 'delete')
    @patch('repositories.database.models.AreasORM.query')
    def test_delete_call_detele_db_function_raise_exception_ok(self, mockFilter, mock):
        mock.side_effect = Mock(
            side_effect=Exception('error'))
        mockFilter.filter_by.return_value.first.return_value = None

        with self.assertRaises(ExceptionDatabase) as context:
            self.dal.delete(
                area=self.area
            )

        self.assertTrue("error" in str(context.exception))
        mock.assert_not_called()

    @patch.object(AreasDAL, 'init_from_orm_to_model')
    @patch('repositories.database.models.AreasORM.query')
    def test_get_id_call_format_inner_function_ok(self, mockFilter, mock):
        mockFilter.filter_by.return_value.first.return_value = self.area_db

        self.dal.get_by_id(
            area=self.id
        )

        mock.assert_called_once()

    @patch.object(AreasDAL, 'init_from_orm_to_model')
    @patch('repositories.database.models.AreasORM.query')
    def test_get_id_returns_none_ok(self, mockFilter, mock):
        mockFilter.filter_by.return_value.first.return_value = None

        result = self.dal.get_by_id(
            area=self.id
        )

        self.assertIsNone(result)
        mock.assert_not_called()

    @patch('repositories.database.models.AreasORM.query')
    def test_get_all_returns_array_ok(self, mockFilter):
        mockFilter.filter_by.return_value.all.return_value = [self.area_db]

        result = self.dal.get_all()
        expected = [
            Area(
                id=self.area_db.id,
                description=self.area_db.description,
                name=self.area_db.name,
                visible=self.area_db.visible,
                date=self.area_db.date
            )
        ]

        self.assertEqual(result, expected)

    @patch('repositories.database.models.AreasORM.query')
    def test_get_all_returns_empty_array_ok(self, mockFilter):
        mockFilter.filter_by.return_value.all.return_value = []

        result = self.dal.get_all()

        self.assertTrue(len(result) == 0)


if __name__ == '__main__':
    unittest.main()
