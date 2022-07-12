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
from patterns.pubsub import PubSubEvent
from domain.models.areas import Area
from domain.observer.topics import CONTROLLER_STATUS
from domain.messages.topics import TOPIC_AREA_SENSORS_STATUS_CONTROLLER
from domain.models.controllers import Controller
from application.services.areas import ServiceAreas
from application.services.controllers import ServiceControllers
from application.services.sensor_data import ServiceSensorsHistoric
from microservices.data_collector.queue_status import QueueState
from microservices.data_collector.data_collector import SensorDataCollector


os.environ['MODE'] = "test"


@unittest.skipUnless(os.getenv('UNIT_TESTS'), 'UNIT TEST')
class SensorDataCollectorUnitTest(unittest.TestCase):

    print('SensorDataCollectorUnitTest...')

    def setUp(self):
        self.observer = Mock()
        self.stop_event = Mock()

        self.topic = "1"
        self.payload = {
            "id": "id"
        }
        self.event = PubSubEvent(
            type=CONTROLLER_STATUS,
            data={
                "topic": self.topic,
                "payload": json.dumps(self.payload),
            }
        )

        self.data_collector = SensorDataCollector(
            stop_event=self.stop_event,
            observer=self.observer,
        )

    # INNER METHODS

    # TESTS
    @patch.object(SensorDataCollector, '_process_controller_status', return_value=True)
    def test_run_calls_inner_threads(self, mock):
        self.data_collector.run()
        mock.assert_called_once()

    @patch.object(queue.Queue, 'put', return_value=True)
    def test_update_save_data_into_local_queue_ok(self, mock):
        self.data_collector.update(
            event=self.event
        )
        mock.assert_called_once_with(
            QueueState(
                topic=self.topic,
                payload=json.dumps(self.payload)
            )
        )

    @patch.object(SensorDataCollector, '_save_controller_state', return_value=True)
    @patch.object(queue.Queue, 'get')
    def test_process_controller_status_does_not_get_data_ok(self, mockQ, mockS):
        status = "asdasdadasd"
        mockQ.side_effect = [
            queue.Empty('asd'), status
        ]

        self.stop_event = MagicMock()
        self.stop_event.is_set.side_effect = [
            False, True
        ]

        self.data_collector = SensorDataCollector(
            stop_event=self.stop_event,
            observer=self.observer,
        )
        self.data_collector.run()

        mockS.assert_not_called()

    @patch.object(SensorDataCollector, '_save_controller_state', return_value=True)
    @patch.object(queue.Queue, 'get')
    def test_process_controller_status_does_get_data_call_save_function_ok(self, mockQ, mockS):
        status = "asdasdadasd"
        mockQ.return_value = status
        self.stop_event = MagicMock()
        self.stop_event.is_set.side_effect = [
            False, True
        ]

        self.data_collector = SensorDataCollector(
            stop_event=self.stop_event,
            observer=self.observer,
        )
        self.data_collector.run()

        mockS.assert_called_once_with(
            data=status
        )

    @patch.object(ServiceSensorsHistoric, 'insert', return_value=True)
    @patch.object(ServiceAreas, 'get_by_id')
    @patch.object(ServiceControllers, 'get_by_id')
    def test_save_status_does_not_insert_area_or_controller_none_ok(self, mockC, mockA, mockS):
        self.area = 500
        self.controller = 4
        self.topic = "asdasdsad"
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

        with self.assertRaises(Exception) as context:
            self.data_collector._save_controller_state(data=self.queue_status)

        self.assertTrue("bad topic format" in str(context.exception))
        mockC.assert_not_called()
        mockA.assert_not_called()
        mockS.assert_not_called()

    @patch.object(ServiceSensorsHistoric, 'insert', return_value=True)
    @patch.object(ServiceAreas, 'get_by_id')
    @patch.object(ServiceControllers, 'get_by_id')
    def test_save_status_does_not_insert_different_area_area_controller_ok(self, mockC, mockA, mockS):
        self.area = 500
        self.controller = 4
        self.description = "a"
        self.name = "a"
        self.visible = True
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

        self.areaC = Area(
            id=self.area,
            description=self.description,
            name=self.name,
            visible=self.visible,
        )

        self.controllerC = Controller(
            id=self.controller,
            area=1,
            description=self.description,
            key=self.name,
            name=self.name,
            visible=self.visible,
        )

        mockC.return_value = self.controllerC
        mockA.return_value = self.areaC

        with self.assertRaises(Exception) as context:
            self.data_collector._save_controller_state(data=self.queue_status)

        self.assertTrue("does not belong to area" in str(context.exception))
        mockC.assert_called_once_with(
            controller=self.controller,
            all_visibility=True
        )
        mockA.assert_called_once_with(
            area=self.area,
            all_visibility=True
        )
        mockS.assert_not_called()

    @patch.object(ServiceSensorsHistoric, 'insert', return_value=True)
    @patch.object(ServiceAreas, 'get_by_id')
    @patch.object(ServiceControllers, 'get_by_id')
    def test_save_status_does_insert_ok(self, mockC, mockA, mockS):
        self.area = 500
        self.controller = 4
        self.description = "a"
        self.name = "a"
        self.visible = True
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

        self.areaC = Area(
            id=self.area,
            description=self.description,
            name=self.name,
            visible=self.visible,
        )

        self.controllerC = Controller(
            id=self.controller,
            area=self.area,
            description=self.description,
            key=self.name,
            name=self.name,
            visible=self.visible,
        )

        mockC.return_value = self.controllerC
        mockA.return_value = self.areaC

        self.data_collector._save_controller_state(data=self.queue_status)

        mockC.assert_called_once_with(
            controller=self.controller,
            all_visibility=True
        )
        mockA.assert_called_once_with(
            area=self.area,
            all_visibility=True
        )
        mockS.assert_called_once()


if __name__ == '__main__':
    unittest.main()
