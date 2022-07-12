# -*- coding: utf-8 -*-
"""
    controllers status observer tests
"""
import json
import os
import queue
import time
import unittest
import uuid
from paho.mqtt.client import MQTTMessage

from unittest.mock import MagicMock, Mock, patch

from settings import messages_settings
from microservices.data_collector.queue_status import QueueState
from domain.messages.topics import TOPIC_AREA_SENSORS_STATUS_CONTROLLER


os.environ['MODE'] = "test"


@unittest.skipUnless(os.getenv('UNIT_TESTS'), 'UNIT TEST')
class QueueStateUnitTest(unittest.TestCase):

    print('QueueStateUnitTest...')

    def setUp(self):
        self.area = 500
        self.controller = 4
        self.topic = TOPIC_AREA_SENSORS_STATUS_CONTROLLER.format(
            area=self.area,
            controller=self.controller,
        )
        self.payload = {
            'id': 'id_test',
            'temperature': {
                'value': 34.6,
                'units': "celsius",
            }
        }

        self.queue_status = QueueState(
            topic=self.topic,
            payload=json.dumps(self.payload),
        )

    # INNER METHODS

    # TESTS
    def test_get_area_queue_status_ok(self):
        self.assertEqual(self.queue_status.get_area(), self.area)

    def test_get_area_queue_status_None_bad_topic_ok(self):
        self.queue_status = QueueState(
            topic="asd",
            payload=json.dumps(self.payload),
        )
        self.assertIsNone(self.queue_status.get_area())

    def test_get_controller_queue_status_ok(self):
        self.assertEqual(self.queue_status.get_controlller(), self.controller)

    def test_get_controller_queue_status_None_bad_topic_ok(self):
        self.queue_status = QueueState(
            topic="asd",
            payload=json.dumps(self.payload),
        )
        self.assertIsNone(self.queue_status.get_controlller())

    def test_get_payload_queue_status_ok(self):
        self.assertEqual(self.queue_status.get_json(), self.payload)


if __name__ == '__main__':
    unittest.main()
