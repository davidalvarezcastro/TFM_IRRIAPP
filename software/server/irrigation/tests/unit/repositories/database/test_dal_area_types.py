# -*- coding: utf-8 -*-
"""
    area types dal tests
"""
from sqlalchemy.exc import DatabaseError
import os
import unittest

from unittest.mock import Mock, patch

from exceptions.database import ExceptionDatabase
from repositories.database.models import TypesORM
from domain.models.area_types import AreaType
from repositories.database.dal.area_types import AreaTypesDAL


os.environ['MODE'] = "test"


@unittest.skipUnless(os.getenv('UNIT_TESTS'), 'UNIT TEST')
class DALTypesUnitTest(unittest.TestCase):

    print('DALTypesUnitTest...')

    def setUp(self):
        self.id = 1
        self.description = "this is a dummy description"

        self.dal = AreaTypesDAL

        self.type = AreaType(
            id=self.id,
            description=self.description,
        )

        self.type_db = TypesORM(
            id=self.id,
            description=self.description,
        )

    # INNER METHODS

    # TESTS
    @patch.object(TypesORM, 'add', return_value=True)
    @patch('repositories.database.dal.area_types.session_scope')
    def test_insert_call_add_db_function_ok(self, mockFilter, mock):
        mockFilter.return_value.__enter__.return_value.query.return_value.filter_by.return_value.first.return_value = \
            None

        type_id = self.dal.insert(
            type=self.type
        )

        mock.assert_called_once()
        self.assertEqual(type_id, self.type.id)

    @patch.object(TypesORM, 'add')
    @patch('repositories.database.dal.area_types.session_scope')
    def test_insert_call_add_db_function_raise_exception_ok(self, mockFilter, mock):
        mock.side_effect = Mock(
            side_effect=Exception('error'))
        mockFilter.return_value.__enter__.return_value.query.return_value.filter_by.return_value.first.return_value = \
            None

        with self.assertRaises(ExceptionDatabase) as context:
            self.dal.insert(
                type=self.type
            )

        self.assertTrue("error" in str(context.exception))
        mock.assert_called_once()

    @patch.object(TypesORM, 'add', return_value=True)
    @patch('repositories.database.dal.area_types.session_scope')
    def test_insert_raise_exception_duplicated_type_ok(self, mockFilter, mock):
        mockFilter.return_value.__enter__.return_value.query.return_value.filter_by.return_value.first.return_value = \
            self.type_db

        with self.assertRaises(ExceptionDatabase) as context:
            self.dal.insert(
                type=self.type
            )

        self.assertTrue(f"Type {self.type.id} duplicated!" in str(context.exception))

        mock.assert_not_called()

    @patch.object(TypesORM, 'update', return_value=True)
    @patch('repositories.database.dal.area_types.session_scope')
    def test_update_call_update_db_function_ok(self, mockFilter, mock):
        mockFilter.return_value.__enter__.return_value.query.return_value.filter_by.return_value.first.return_value = \
            self.type_db

        self.dal.update(
            type=self.type
        )

        mock.assert_called_once()

    @patch.object(TypesORM, 'update')
    @patch('repositories.database.dal.area_types.session_scope')
    def test_update_call_update_db_function_raise_exception_ok(self, mockFilter, mock):
        mock.side_effect = Mock(
            side_effect=Exception('error'))
        mockFilter.return_value.__enter__.return_value.query.return_value.filter_by.return_value.first.return_value = \
            self.type_db

        with self.assertRaises(ExceptionDatabase) as context:
            self.dal.update(
                type=self.type
            )

        self.assertTrue("error" in str(context.exception))
        mock.assert_called_once()

    @patch.object(TypesORM, 'add', return_value=True)
    @patch('repositories.database.dal.area_types.session_scope')
    def test_update_raise_exception_no_type_saved_ok(self, mockFilter, mock):
        mockFilter.return_value.__enter__.return_value.query.return_value.filter_by.return_value.first.return_value = \
            None

        with self.assertRaises(ExceptionDatabase) as context:
            self.dal.update(
                type=self.type
            )

        self.assertTrue(f"Type {self.type.id} is not saved!" in str(context.exception))

        mock.assert_not_called()

    @patch.object(TypesORM, 'delete', return_value=True)
    @patch('repositories.database.dal.area_types.session_scope')
    def test_delete_call_delete_db_function_ok(self, mockFilter, mock):
        mockFilter.return_value.__enter__.return_value.query.return_value.filter_by.return_value.first.return_value = \
            self.type_db

        self.dal.delete(
            type=self.type
        )

        mock.assert_called_once()

    @patch.object(TypesORM, 'delete')
    @patch('repositories.database.dal.area_types.session_scope')
    def test_delete_call_detele_db_function_raise_exception_ok(self, mockFilter, mock):
        mock.side_effect = Mock(
            side_effect=Exception('error'))
        mockFilter.return_value.__enter__.return_value.query.return_value.filter_by.return_value.first.return_value = \
            None

        with self.assertRaises(ExceptionDatabase) as context:
            self.dal.delete(
                type=self.type
            )

        self.assertTrue("error" in str(context.exception))
        mock.assert_not_called()

    @patch.object(AreaTypesDAL, 'init_from_orm_to_model')
    @patch('repositories.database.dal.area_types.session_scope')
    def test_get_id_call_format_inner_function_ok(self, mockFilter, mock):
        mockFilter.return_value.__enter__.return_value.query.return_value.filter_by.return_value.first.return_value = \
            self.type_db

        self.dal.get_by_id(
            type=self.id
        )

        mock.assert_called_once()

    @patch.object(AreaTypesDAL, 'init_from_orm_to_model')
    @patch('repositories.database.dal.area_types.session_scope')
    def test_get_id_returns_none_ok(self, mockFilter, mock):
        mockFilter.return_value.__enter__.return_value.query.return_value.filter_by.return_value.first.return_value = \
            None

        result = self.dal.get_by_id(
            type=self.id
        )

        self.assertIsNone(result)
        mock.assert_not_called()

    @patch.object(AreaTypesDAL, 'init_from_orm_to_model')
    @patch('repositories.database.dal.area_types.session_scope')
    def test_get_id_returns_none_database_exception_ok(self, mockFilter, mock):
        mockFilter.return_value.__enter__.return_value.query.return_value.filter_by.return_value.first.side_effect = \
            Mock(
                side_effect=DatabaseError(
                    statement=None,
                    params=None,
                    orig=None,
                    ismulti=False,
                ))

        result = self.dal.get_by_id(
            type=self.id
        )

        self.assertIsNone(result)
        mock.assert_not_called()

    @patch('repositories.database.dal.area_types.session_scope')
    def test_get_all_returns_array_ok(self, mockFilter):
        mockFilter.return_value.__enter__.return_value.query.return_value.filter.return_value.all.return_value = [
            self.type_db]

        result = self.dal.get_all()
        expected = [
            AreaType(
                id=self.type_db.id,
                description=self.type_db.description,
            )
        ]

        self.assertEqual(result, expected)

    @patch('repositories.database.dal.area_types.session_scope')
    def test_get_all_returns_empty_array_ok(self, mockFilter):
        mockFilter.return_value.__enter__.return_value.query.return_value.filter.return_value.all.return_value = []

        result = self.dal.get_all()

        self.assertTrue(len(result) == 0)

    @patch('repositories.database.dal.area_types.session_scope')
    def test_get_all_returns_empty_array_database_exception_ok(self, mockFilter):
        mockFilter.return_value.__enter__.return_value.query.return_value.filter.return_value.all.side_effect = \
            Mock(
                side_effect=DatabaseError(
                    statement=None,
                    params=None,
                    orig=None,
                    ismulti=False,
                ))

        result = self.dal.get_all()

        self.assertTrue(len(result) == 0)


if __name__ == '__main__':
    unittest.main()
