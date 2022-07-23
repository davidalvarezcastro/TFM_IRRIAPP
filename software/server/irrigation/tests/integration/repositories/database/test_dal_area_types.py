# -*- coding: utf-8 -*-
"""
    area types dal tests
"""
import os
import unittest

from exceptions.database import ExceptionDatabase
from repositories.database.models import TypesORM
from domain.models.area_types import AreaType
from repositories.database.dal.area_types import AreaTypesDAL


os.environ['MODE'] = "test"


@unittest.skipUnless(os.getenv('INTEGRATION_TESTS'), 'INTEGRATION TEST')
class DALTypesIntegrationTest(unittest.TestCase):

    print('DALTypesIntegrationTest...')

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

        # clean data table
        TypesORM.query.delete()

    # INNER METHODS

    # TESTS
    def test_insert_function_add_element_database_ok(self):
        expected_previous = TypesORM.query.filter_by(id=self.type.id).first()

        type_id = self.dal.insert(
            type=self.type
        )

        expected = TypesORM.query.filter_by(id=self.type.id).first()
        self.assertIsNone(expected_previous)
        self.assertIsNotNone(expected)
        self.assertEqual(type_id, self.type.id)
        self.assertEqual(expected.id, self.type.id)
        self.assertEqual(expected.description, self.description)

    def test_insert_function_add_element_database_return_new_id_ok(self):
        expected_previous = TypesORM.query.filter_by(id=self.type.id).first()
        self.type = AreaType(
            description=self.description,
        )

        type_id = self.dal.insert(
            type=self.type
        )

        expected = TypesORM.query.filter_by(id=self.type.id).first()
        self.assertIsNone(expected_previous)
        self.assertIsNotNone(expected)
        self.assertEqual(type_id, self.type.id)
        self.assertEqual(expected.id, self.type.id)
        self.assertEqual(expected.description, self.description)

    def test_insert_function_raise_exception_duplicated_element_ok(self):
        self.type_db.add()

        with self.assertRaises(ExceptionDatabase) as context:
            self.dal.insert(
                type=self.type
            )

        expected = TypesORM.query.filter_by(id=self.type.id).first()
        self.assertTrue(f"Type {self.type.id} duplicated!" in str(context.exception))
        self.assertIsNotNone(expected)

    def test_update_function_update_element_database_ok(self):
        description = "new description"
        self.type_db.add()

        self.type.description = description
        self.dal.update(
            type=self.type
        )

        expected = TypesORM.query.filter_by(id=self.type.id).first()
        self.assertIsNotNone(expected)
        self.assertEqual(expected.id, self.type.id)
        self.assertEqual(expected.description, description)

    def test_update_function_raise_exception_element_none_ok(self):
        with self.assertRaises(ExceptionDatabase) as context:
            self.dal.update(
                type=self.type
            )

        expected = TypesORM.query.filter_by(id=self.type.id).first()
        self.assertTrue(f"Type {self.type.id} is not saved!" in str(context.exception))
        self.assertIsNone(expected)

    def test_delete_function_remove_element_database_ok(self):
        self.type_db.add()

        expected_previous = TypesORM.query.filter_by(id=self.type.id).first()

        self.dal.delete(
            type=self.type
        )

        expected = TypesORM.query.filter_by(id=self.type.id).first()
        self.assertIsNotNone(expected_previous)
        self.assertIsNone(expected)

    def test_get_id_function_return_element_by_id_ok(self):
        self.type_db.add()

        expected_id = self.type_db.id
        expected_description = self.type_db.description

        self.id = 3
        self.description = "new area type"
        self.type_db = TypesORM(
            id=self.id,
            description=self.description,
        )

        self.type_db.add()

        result = self.dal.get_by_id(
            type=expected_id
        )

        self.assertIsNotNone(result)
        self.assertEqual(result.id, expected_id)
        self.assertEqual(result.description, expected_description)

    def test_get_id_function_return_none_ok(self):
        self.type_db.add()
        self.id = 3

        result = self.dal.get_by_id(
            type=self.id
        )

        self.assertIsNone(result)

    def test_get_all_function_return_array_ok(self):
        self.type_db.add()
        self.id = 2
        self.description = "description 2"
        self.type_db = TypesORM(
            id=self.id,
            description=self.description,
        )
        self.type_db.add()

        result = self.dal.get_all()

        self.assertIsNotNone(result)
        self.assertTrue(len(result) == 2)

    def test_get_all_function_return_empty_array_ok(self):
        result = self.dal.get_all()

        self.assertIsNotNone(result)
        self.assertTrue(len(result) == 0)


if __name__ == '__main__':
    unittest.main()
