# -*- coding: utf-8 -*-
"""
    controllers dal tests
"""
import datetime
import json
import os
import time
import unittest

from unittest.mock import Mock, patch

from exceptions.database import ExceptionDatabase
from domain.models.controllers import Controller
from repositories.database.models import AreasORM, ControllersORM
from repositories.database.dal.controllers import ControllersDAL


os.environ['MODE'] = "test"


@unittest.skipUnless(os.getenv('INTEGRATION_TESTS'), 'INTEGRATION TEST')
class DALControllersIntegrationTest(unittest.TestCase):

    print('DALControllersIntegrationTest...')

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

        self.area_db = AreasORM(
            id=self.area,
            description="testing",
            name="testing",
            visible=self.visible,
        )

        # clean data table
        AreasORM.query.delete()
        ControllersORM.query.delete()
        self.area_db.add()

    # INNER METHODS

    # TESTS
    def test_insert_function_add_element_database_ok(self):
        expected_previous = ControllersORM.query.filter_by(id=self.controller.id).first()

        controller_id = self.dal.insert(
            controller=self.controller
        )

        expected = ControllersORM.query.filter_by(id=self.controller.id).first()
        self.assertIsNone(expected_previous)
        self.assertIsNotNone(expected)
        self.assertEqual(controller_id, self.controller.id)
        self.assertEqual(expected.id, self.controller.id)
        self.assertEqual(expected.description, self.description)
        self.assertEqual(expected.name, self.name)

    def test_insert_function_add_element_database_return_new_id_ok(self):
        expected_previous = ControllersORM.query.filter_by(id=self.controller.id).first()
        self.controller = Controller(
            id=1,
            area=self.area,
            description=self.description,
            key=self.key,
            name=self.name,
            visible=self.visible,
        )

        controller_id = self.dal.insert(
            controller=self.controller
        )

        expected = ControllersORM.query.filter_by(id=self.controller.id).first()
        self.assertIsNone(expected_previous)
        self.assertIsNotNone(expected)
        self.assertEqual(controller_id, self.controller.id)
        self.assertEqual(expected.id, self.controller.id)
        self.assertEqual(expected.description, self.description)
        self.assertEqual(expected.name, self.name)

    def test_insert_function_raise_exception_duplicated_element_ok(self):
        self.controller_db.add()

        with self.assertRaises(ExceptionDatabase) as context:
            self.dal.insert(
                controller=self.controller
            )

        expected = ControllersORM.query.filter_by(id=self.controller.id).first()
        self.assertTrue(f"Controller {self.controller.id} duplicated!" in str(context.exception))
        self.assertIsNotNone(expected)

    def test_update_function_update_element_database_ok(self):
        description = "new description"
        active = 0
        name = "test_name"
        self.controller_db.add()

        self.controller.description = description
        self.controller.visible = active
        self.controller.name = name
        self.dal.update(
            controller=self.controller
        )

        expected = ControllersORM.query.filter_by(id=self.controller.id).first()
        self.assertIsNotNone(expected)
        self.assertEqual(expected.id, self.controller.id)
        self.assertEqual(expected.description, description)
        self.assertEqual(expected.visible, active)
        self.assertEqual(expected.name, name)

    def test_update_function_raise_exception_element_none_ok(self):
        with self.assertRaises(ExceptionDatabase) as context:
            self.dal.update(
                controller=self.controller
            )

        expected = ControllersORM.query.filter_by(id=self.controller.id).first()
        self.assertTrue(f"Controller {self.controller.id} is not saved!" in str(context.exception))
        self.assertIsNone(expected)

    def test_delete_function_remove_element_database_ok(self):
        self.controller_db.add()

        expected_previous = ControllersORM.query.filter_by(id=self.controller.id).first()

        self.dal.delete(
            controller=self.controller
        )

        expected = ControllersORM.query.filter_by(id=self.controller.id).first()
        self.assertIsNotNone(expected_previous)
        self.assertIsNone(expected)

    def test_get_id_function_return_element_by_id_ok(self):
        self.controller_db.add()

        result = self.dal.get_by_id(
            controller=self.controller_db.id
        )

        self.assertIsNotNone(result)
        self.assertEqual(result.id, self.controller_db.id)
        self.assertEqual(result.description, self.controller_db.description)
        self.assertEqual(result.name, self.controller_db.name)

    def test_get_id_function_not_return_element_not_visible_ok(self):
        self.controller_db = ControllersORM(
            id=self.id,
            area=self.area,
            description=self.description,
            key=self.key,
            name=self.name,
            visible=False,
        )

        self.controller_db.add()

        result = self.dal.get_by_id(
            controller=self.controller_db.id,
            all_visibility=False
        )

        self.assertIsNone(result)

    def test_get_id_function_return_element_not_visible_ok(self):
        self.controller_db.visible = False
        self.controller_db.add()

        result = self.dal.get_by_id(
            controller=self.controller_db.id,
            all_visibility=True
        )

        self.assertIsNotNone(result)
        self.assertEqual(result.id, self.controller_db.id)
        self.assertEqual(result.description, self.controller_db.description)
        self.assertEqual(result.name, self.controller_db.name)

    def test_get_id_function_return_none_ok(self):
        self.controller_db.add()
        self.id = 3

        result = self.dal.get_by_id(
            controller=self.id
        )

        self.assertIsNone(result)

    def test_get_all_function_return_array__all_visibility_ok(self):
        self.controller_db.add()
        self.id = 2
        self.description = "description 2"
        self.controller_db = ControllersORM(
            id=self.id,
            area=self.area,
            description=self.description,
            key=self.key,
            name=self.name,
            visible=False,
        )
        self.controller_db.add()

        result = self.dal.get_all(
            all_visibility=True
        )

        self.assertIsNotNone(result)
        self.assertTrue(len(result) == 2)

    def test_get_all_function_return_array_only_visibles_ok(self):
        self.controller_db.add()
        self.id = 2
        self.description = "description 2"
        self.controller_db = ControllersORM(
            id=self.id,
            area=self.area,
            description=self.description,
            key=self.key,
            name=self.name,
            visible=False,
        )
        self.controller_db.add()

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
