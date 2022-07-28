# -*- coding: utf-8 -*-
"""
    simple actuator activation algorithm
"""
import json
import os
import queue
import time
import unittest
import uuid
from paho.mqtt.client import MQTTMessage

from unittest.mock import MagicMock, Mock, patch

from domain.models.irrigation_actuator_algorithm import IrrigationActivateActuator
from application.actuator.models.simple_actuator_irrigation import SimpleActuatorIrirgationHandler


os.environ['MODE'] = "test"


@unittest.skipUnless(os.getenv('UNIT_TESTS'), 'UNIT TEST')
class SimpleActuatorIrirgationHandlerUnitTest(unittest.TestCase):

    print('SimpleActuatorIrirgationHandlerUnitTest...')

    def setUp(self):
        self.strategy = SimpleActuatorIrirgationHandler()

    # INNER METHODS

    # TESTS
    def test_hight_temperature_high_humidity_return_false_ok(self):
        expected = False
        self.query = IrrigationActivateActuator(
            rainning=2,
            humidity=70,
            temperature=35,
        )

        result = self.strategy.check_activate_irrigation(
            query=self.query
        )
        self.assertEqual(result, expected)

    def test_rained_ignore_humidity_temperature_return_false_ok(self):
        expected = False
        self.query = IrrigationActivateActuator(
            rainning=100,
            humidity=10,
            temperature=30,
        )

        result = self.strategy.check_activate_irrigation(
            query=self.query
        )
        self.assertEqual(result, expected)

    def test_low_temperature_high_humidity_return_false_ok(self):
        expected = False
        self.query = IrrigationActivateActuator(
            rainning=0,
            humidity=80,
            temperature=10,
        )

        result = self.strategy.check_activate_irrigation(
            query=self.query
        )
        self.assertEqual(result, expected)

    def test_high_temperature_low_humidity_return_true_ok(self):
        expected = True
        self.query = IrrigationActivateActuator(
            rainning=0,
            humidity=25,
            temperature=28,
        )

        result = self.strategy.check_activate_irrigation(
            query=self.query
        )
        self.assertEqual(result, expected)

    def test_very_high_temperature_normal_humidity_return_false_ok(self):
        expected = False
        self.query = IrrigationActivateActuator(
            rainning=0,
            humidity=50,
            temperature=37,
        )

        result = self.strategy.check_activate_irrigation(
            query=self.query
        )
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
