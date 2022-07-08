# -*- coding: utf-8 -*-
"""
    areas dal tests
"""
import os
import unittest

from exceptions.database import ExceptionDatabase
from domain.models.areas import Area
from repositories.database.models import AreasORM
from repositories.database.dal.areas import AreasDAL


os.environ['MODE'] = "test"


@unittest.skipUnless(os.getenv('INTEGRATION_TESTS'), 'INTEGRATION TEST')
class DALAreasIntegrationTest(unittest.TestCase):

    print('DALAreasIntegrationTest...')

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

        # clean data table
        AreasORM.query.delete()

    # INNER METHODS

    # TESTS
    def test_insert_function_add_element_database_ok(self):
        expected_previous = AreasORM.query.filter_by(id=self.area.id).first()

        self.area = Area(
            id=1,
            description=self.description,
            name=self.name,
            visible=self.visible,
        )

        area_id = self.dal.insert(
            area=self.area
        )

        expected = AreasORM.query.filter_by(id=self.area.id).first()
        self.assertIsNone(expected_previous)
        self.assertIsNotNone(expected)
        self.assertEqual(area_id, self.area.id)
        self.assertEqual(expected.id, self.area.id)
        self.assertEqual(expected.description, self.description)
        self.assertEqual(expected.name, self.name)

    def test_insert_function_add_element_database_return_new_id_ok(self):
        expected_previous = AreasORM.query.filter_by(id=self.area.id).first()

        area_id = self.dal.insert(
            area=self.area
        )

        expected = AreasORM.query.filter_by(id=self.area.id).first()
        self.assertIsNone(expected_previous)
        self.assertIsNotNone(expected)
        self.assertEqual(area_id, self.area.id)
        self.assertEqual(expected.id, self.area.id)
        self.assertEqual(expected.description, self.description)
        self.assertEqual(expected.name, self.name)

    def test_insert_function_raise_exception_duplicated_element_ok(self):
        self.area_db.add()

        with self.assertRaises(ExceptionDatabase) as context:
            self.dal.insert(
                area=self.area
            )

        expected = AreasORM.query.filter_by(id=self.area.id).first()
        self.assertTrue(f"Area {self.area.id} duplicated!" in str(context.exception))
        self.assertIsNotNone(expected)

    def test_update_function_update_element_database_ok(self):
        description = "new description"
        active = 0
        name = "test_name"
        self.area_db.add()

        self.area.description = description
        self.area.visible = active
        self.area.name = name
        self.dal.update(
            area=self.area
        )

        expected = AreasORM.query.filter_by(id=self.area.id).first()
        self.assertIsNotNone(expected)
        self.assertEqual(expected.id, self.area.id)
        self.assertEqual(expected.description, description)
        self.assertEqual(expected.visible, active)
        self.assertEqual(expected.name, name)

    def test_update_function_raise_exception_element_none_ok(self):
        with self.assertRaises(ExceptionDatabase) as context:
            self.dal.update(
                area=self.area
            )

        expected = AreasORM.query.filter_by(id=self.area.id).first()
        self.assertTrue(f"Area {self.area.id} is not saved!" in str(context.exception))
        self.assertIsNone(expected)

    def test_delete_function_remove_element_database_ok(self):
        self.area_db.add()

        expected_previous = AreasORM.query.filter_by(id=self.area.id).first()

        self.dal.delete(
            area=self.area
        )

        expected = AreasORM.query.filter_by(id=self.area.id).first()
        self.assertIsNotNone(expected_previous)
        self.assertIsNone(expected)

    def test_get_id_function_return_element_by_id_ok(self):
        self.area_db.add()

        result = self.dal.get_by_id(
            area=self.area_db.id
        )

        self.assertIsNotNone(result)
        self.assertEqual(result.id, self.area_db.id)
        self.assertEqual(result.description, self.area_db.description)
        self.assertEqual(result.name, self.area_db.name)

    def test_get_id_function_not_return_element_not_visible_ok(self):
        self.area_db = AreasORM(
            id=self.id,
            description=self.description,
            name=self.name,
            visible=False,
        )

        self.area_db.add()

        result = self.dal.get_by_id(
            area=self.area_db.id,
            all_visibility=False
        )

        self.assertIsNone(result)

    def test_get_id_function_return_element_not_visible_ok(self):
        self.area_db.visible = False
        self.area_db.add()

        result = self.dal.get_by_id(
            area=self.area_db.id,
            all_visibility=True
        )

        self.assertIsNotNone(result)
        self.assertEqual(result.id, self.area_db.id)
        self.assertEqual(result.description, self.area_db.description)
        self.assertEqual(result.name, self.area_db.name)

    def test_get_id_function_return_none_ok(self):
        self.area_db.add()
        self.id = 3

        result = self.dal.get_by_id(
            area=self.id
        )

        self.assertIsNone(result)

    def test_get_all_function_return_array_all_visibility_ok(self):
        self.area_db.add()
        self.id = 2
        self.description = "description 2"
        self.name = "testing"
        self.area_db = AreasORM(
            id=self.id,
            description=self.description,
            name=self.name,
        )
        self.area_db.add()

        result = self.dal.get_all(
            all_visibility=True
        )

        self.assertIsNotNone(result)
        self.assertTrue(len(result) == 2)

    def test_get_all_function_return_array_only_visible_ok(self):
        self.area_db.add()
        self.id = 2
        self.description = "description 2"
        self.name = "testing"
        area_db = AreasORM(
            id=self.id,
            description=self.description,
            name=self.name,
            visible=False
        )
        area_db.add()

        result = self.dal.get_all(
            all_visibility=False
        )

        self.assertIsNotNone(result)
        self.assertTrue(len(result) == 1)

    def test_get_all_function_return_empty_array_ok(self):
        expected = []
        result = self.dal.get_all()

        self.assertIsNotNone(result)
        self.assertTrue(len(result) == 0)
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
