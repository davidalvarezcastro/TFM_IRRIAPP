# -*- coding: utf-8 -*-
"""
    microservice sensor data processor (actuator activation check)
    TODO:
"""
import datetime
import json
import os
import queue
from this import d
import time
import unittest
import uuid

from unittest.mock import MagicMock, Mock, PropertyMock, patch

from patterns.pubsub import PubSubEvent
from domain.models.areas import Area
from domain.observer.topics import ACTUATOR_RELAY_ON_OK, ACTUATOR_RELAY_OFF_OK
from domain.messages.topics import TOPIC_AREA_ACTUATOR_RELAY_OFF_CONFIRMATION, TOPIC_AREA_ACTUATOR_RELAY_ON_CONFIRMATION
from domain.messages.services import MessagesServices
from domain.models.controllers import Controller
from application.services.areas import ServiceAreas
from application.services.controllers import ServiceControllers
from application.services.sensor_data import ServiceSensorsHistoric
from domain.models.sensor_data_historic import SensorData
from application.services.irrigation_data import ServiceIrrigationHistoric
from domain.models.irrigation_actuator_algorithm import IrrigationActivateActuator
from microservices.actuator_controller.queue_status import QueueState
from microservices.actuator_controller.data_processor import SensorDataProcessor
from application.actuator.models.simple_actuator_irrigation import SimpleActuatorIrirgationHandler


os.environ['MODE'] = "test"


@unittest.skipUnless(os.getenv('UNIT_TESTS'), 'UNIT TEST')
class SensorDataProcessorUnitTest(unittest.TestCase):

    print('SensorDataProcessorUnitTest...')

    def setUp(self):
        self.observer = Mock()
        self.stop_event = Mock()
        self.pusblisher = Mock()
        self.strategy = Mock()

        self.area = Area(
            id=1,
            visible=True,
            name="name1",
            description="old",
        )
        self.topic_on = TOPIC_AREA_ACTUATOR_RELAY_ON_CONFIRMATION.format(area=self.area.id)
        self.topic_off = TOPIC_AREA_ACTUATOR_RELAY_OFF_CONFIRMATION.format(area=self.area.id)
        self.payload = {}
        self.event_on_confirmation = PubSubEvent(
            type=ACTUATOR_RELAY_ON_OK,
            data={
                "topic": self.topic_on,
                "payload": json.dumps(self.payload),
            }
        )
        self.event_off_confirmation = PubSubEvent(
            type=ACTUATOR_RELAY_OFF_OK,
            data={
                "topic": self.topic_off,
                "payload": json.dumps(self.payload),
            }
        )

        self.data_processor = SensorDataProcessor(
            stop_event=self.stop_event,
            observer=self.observer,
            pusblisher=self.pusblisher,
            actuator_strategy=self.strategy
        )

    # INNER METHODS

    # TESTS
    @patch.object(SensorDataProcessor, '_control_actuator_sensor_data', return_value=True)
    def test_run_calls_inner_threads(self, mock):
        self.data_processor.run()
        mock.assert_called_once()

    @patch.object(queue.Queue, 'put', return_value=True)
    def test_update_save_data_into_local_queue_on_confirmation_ok(self, mock):
        self.data_processor.update(
            event=self.event_on_confirmation
        )
        mock.assert_called_once_with(
            QueueState(
                type=ACTUATOR_RELAY_ON_OK,
                topic=self.topic_on,
                payload=json.dumps(self.payload)
            )
        )

    @patch.object(queue.Queue, 'put', return_value=True)
    def test_update_save_data_into_local_queue_off_confirmation_ok(self, mock):
        self.data_processor.update(
            event=self.event_off_confirmation
        )
        mock.assert_called_once_with(
            QueueState(
                type=ACTUATOR_RELAY_OFF_OK,
                topic=self.topic_off,
                payload=json.dumps(self.payload)
            )
        )

    @patch.object(ServiceControllers, 'get_by_area')
    @patch.object(ServiceSensorsHistoric, 'get_last')
    @patch.object(ServiceSensorsHistoric, 'get')
    def test_summary_sensor_data_return_summary_ok_1(
            self, mockHistorical, mockLastSensorData, mockGetControllers):
        self.controller = Controller(
            id=1,
            area=self.area.id,
            visible=True,
            name="name1",
            description="old",
        )
        self.sensor_data = SensorData(
            area_id=self.area.id,
            controller_id=1,
            area="name1",
            controller="name1",
            humidity=20,
            temperature=20,
            raining=True,
            date=datetime.datetime(2022, 7, 29, 21, 00, 00, 0)
        )
        expected = IrrigationActivateActuator(
            rainning=100.0,
            humidity=self.sensor_data.humidity,
            temperature=self.sensor_data.temperature,
        )

        mockGetControllers.return_value = [
            self.controller
        ]
        mockLastSensorData.return_value = self.sensor_data
        mockHistorical.return_value = [
            self.sensor_data, self.sensor_data
        ]

        summary = self.data_processor._get_summary_sensor_data_area(
            area=self.area
        )

        self.assertEqual(summary, expected)

    @patch.object(ServiceControllers, 'get_by_area')
    @patch.object(ServiceSensorsHistoric, 'get_last')
    @patch.object(ServiceSensorsHistoric, 'get')
    def test_summary_sensor_data_no_last_data_return_summary_ok(
            self, mockHistorical, mockLastSensorData, mockGetControllers):
        self.controller = Controller(
            id=1,
            area=self.area.id,
            visible=True,
            name="name1",
            description="old",
        )
        self.sensor_data = SensorData(
            area_id=self.area.id,
            controller_id=1,
            area="name1",
            controller="name1",
            humidity=20,
            temperature=20,
            raining=True,
            date=datetime.datetime(2022, 7, 29, 21, 00, 00, 0)
        )
        expected = IrrigationActivateActuator(
            rainning=100.0,
            humidity=self.sensor_data.humidity,
            temperature=self.sensor_data.temperature,
        )

        mockGetControllers.return_value = [
            self.controller
        ]
        # error getting last sensor data but it has data from 24 hours ago
        mockLastSensorData.return_value = None
        mockHistorical.return_value = [
            self.sensor_data, self.sensor_data
        ]

        expected = IrrigationActivateActuator(
            rainning=100.0,
            humidity=0,
            temperature=0,
        )

        summary = self.data_processor._get_summary_sensor_data_area(
            area=self.area
        )

        self.assertEqual(summary, expected)

    @patch.object(ServiceControllers, 'get_by_area')
    @patch.object(ServiceSensorsHistoric, 'get_last')
    @patch.object(ServiceSensorsHistoric, 'get')
    def test_summary_sensor_data_no_24_hours_data_return_summary_ok(
            self, mockHistorical, mockLastSensorData, mockGetControllers):
        self.controller = Controller(
            id=1,
            area=self.area.id,
            visible=True,
            name="name1",
            description="old",
        )
        self.sensor_data = SensorData(
            area_id=self.area.id,
            controller_id=1,
            area="name1",
            controller="name1",
            humidity=20,
            temperature=20,
            raining=True,
            date=datetime.datetime(2022, 7, 29, 21, 00, 00, 0)
        )
        expected = IrrigationActivateActuator(
            rainning=0,
            humidity=self.sensor_data.humidity,
            temperature=self.sensor_data.temperature,
        )

        mockGetControllers.return_value = [
            self.controller
        ]
        mockLastSensorData.return_value = self.sensor_data
        mockHistorical.return_value = []

        summary = self.data_processor._get_summary_sensor_data_area(
            area=self.area
        )

        self.assertEqual(summary, expected)

    @patch.object(ServiceControllers, 'get_by_area')
    @patch.object(ServiceSensorsHistoric, 'get_last')
    @patch.object(ServiceSensorsHistoric, 'get')
    def test_summary_sensor_data_no_controllers_return_summary_ok(
            self, mockHistorical, mockLastSensorData, mockGetControllers):
        expected = None

        mockGetControllers.return_value = []

        summary = self.data_processor._get_summary_sensor_data_area(
            area=self.area
        )

        self.assertEqual(summary, expected)

    @patch.object(queue.Queue, 'get')
    def test_wait_for_confirmation_relay_on_return_true_data_in_queue_ok(self, mockQ):
        expected = True
        self.queue_state = QueueState(
            type=ACTUATOR_RELAY_ON_OK,
            topic="",
            payload=""
        )

        mockQ.side_effect = [
            queue.Empty('asd'), self.queue_state
        ]

        result = self.data_processor._wait_for_confirmation_from_actuator(
            area=self.area.id,
            mode_on=True
        )

        self.assertEqual(result, expected)

    @patch.object(queue.Queue, 'get')
    def test_wait_for_confirmation_relay_off_return_true_data_in_queue_ok(self, mockQ):
        expected = True
        self.queue_state = QueueState(
            type=ACTUATOR_RELAY_OFF_OK,
            topic="",
            payload=""
        )

        mockQ.side_effect = [
            queue.Empty('asd'), self.queue_state
        ]

        result = self.data_processor._wait_for_confirmation_from_actuator(
            area=self.area.id,
            mode_on=False
        )

        self.assertEqual(result, expected)

    @patch.object(queue.Queue, 'get')
    def test_wait_for_confirmation_relay_on_return_falsa_no_confirmation_ok(self, mockQ):
        expected = False
        self.queue_state = QueueState(
            type=ACTUATOR_RELAY_ON_OK,
            topic="",
            payload=""
        )

        mockQ.side_effect = [
            queue.Empty('asd'), queue.Empty('asd'), queue.Empty('asd')
        ]

        result = self.data_processor._wait_for_confirmation_from_actuator(
            area=self.area.id,
            mode_on=True
        )

        self.assertEqual(result, expected)

    @patch.object(queue.Queue, 'get')
    def test_wait_for_confirmation_relay_off_return_false_no_confirmation_ok(self, mockQ):
        expected = False
        self.queue_state = QueueState(
            type=ACTUATOR_RELAY_OFF_OK,
            topic="",
            payload=""
        )

        mockQ.side_effect = [
            queue.Empty('asd'), queue.Empty('asd'), queue.Empty('asd')
        ]

        result = self.data_processor._wait_for_confirmation_from_actuator(
            area=self.area.id,
            mode_on=False
        )

        self.assertEqual(result, expected)

    @patch.object(MessagesServices, 'pub_relay_on', return_value=True)
    @patch.object(SensorDataProcessor, '_wait_for_confirmation_from_actuator')
    @patch.object(ServiceIrrigationHistoric, 'insert')
    def test_handle_activate_actuator_receive_confirmation_insert_data_ok(
            self, mock, mockConfirmation, mockPub):
        expected = True
        mockConfirmation.return_value = expected
        result = self.data_processor._handle_activate_actuator(
            area=self.area
        )

        mock.assert_called_once()
        self.assertEqual(result, expected)

    @patch.object(MessagesServices, 'pub_relay_on', return_value=True)
    @patch.object(SensorDataProcessor, '_wait_for_confirmation_from_actuator')
    @patch.object(ServiceIrrigationHistoric, 'insert')
    def test_handle_activate_actuator_not_receive_confirmation_not_insert_data_ok(
            self, mock, mockConfirmation, mockPub):
        expected = False
        mockConfirmation.return_value = expected
        result = self.data_processor._handle_activate_actuator(
            area=self.area
        )

        mock.assert_not_called()
        self.assertEqual(result, expected)

    @patch.object(MessagesServices, 'pub_relay_off', return_value=True)
    @patch.object(SensorDataProcessor, '_wait_for_confirmation_from_actuator')
    @patch.object(ServiceIrrigationHistoric, 'end_irrigation')
    def test_handle_desactivate_actuator_receive_confirmation_end_irrigation_ok(
            self, mock, mockConfirmation, mockPub):
        expected = True
        mockConfirmation.return_value = expected
        result = self.data_processor._handle_desactivate_actuator(
            area=self.area
        )

        mock.assert_called_once()
        self.assertEqual(result, expected)

    @patch.object(MessagesServices, 'pub_relay_off', return_value=True)
    @patch.object(SensorDataProcessor, '_wait_for_confirmation_from_actuator')
    @patch.object(ServiceIrrigationHistoric, 'end_irrigation')
    def test_handle_desactivate_actuator_not_receive_confirmation_not_insert_data_ok(
            self, mock, mockConfirmation, mockPub):
        expected = False
        mockConfirmation.return_value = expected
        result = self.data_processor._handle_desactivate_actuator(
            area=self.area
        )

        mock.assert_not_called()
        self.assertEqual(result, expected)

    @patch.object(ServiceAreas, 'get_all')
    @patch.object(SensorDataProcessor, '_get_summary_sensor_data_area')
    @patch.object(SensorDataProcessor, '_handle_activate_actuator')
    def test_control_actuator_sensor_data_needs_to_activate_actuator_call_handler_once_ok(
            self, mock, mockSummary, mockAreas):
        self.sensor_data = SensorData(
            area_id=self.area.id,
            controller_id=1,
            area="name1",
            controller="name1",
            humidity=10,
            temperature=20,
            raining=True,
            date=datetime.datetime(2022, 7, 29, 21, 00, 00, 0)
        )

        self.stop_event = MagicMock()
        self.stop_event.is_set.side_effect = [
            False, True
        ]

        mockAreas.return_value = [
            self.area
        ]

        mockSummary.return_value = IrrigationActivateActuator(
            rainning=0,
            humidity=self.sensor_data.humidity,
            temperature=self.sensor_data.temperature,
        )

        self.strategy = SimpleActuatorIrirgationHandler()
        self.data_processor = SensorDataProcessor(
            stop_event=self.stop_event,
            observer=self.observer,
            pusblisher=self.pusblisher,
            actuator_strategy=self.strategy
        )

        self.data_processor._control_actuator_sensor_data()

        mock.assert_called_once_with(
            area=self.area
        )

    @patch.object(ServiceAreas, 'get_all')
    @patch.object(SensorDataProcessor, '_get_summary_sensor_data_area')
    @patch.object(SensorDataProcessor, '_handle_activate_actuator')
    def test_control_actuator_sensor_data_needs_to_activate_actuator_many_times_call_handler_once_ok(
            self, mock, mockSummary, mockAreas):
        self.sensor_data = SensorData(
            area_id=self.area.id,
            controller_id=1,
            area="name1",
            controller="name1",
            humidity=10,
            temperature=20,
            raining=True,
            date=datetime.datetime(2022, 7, 29, 21, 00, 00, 0)
        )

        self.stop_event = MagicMock()
        self.stop_event.is_set.side_effect = [
            False, False, True
        ]

        mock.return_value = True

        mockAreas.return_value = [
            self.area
        ]

        mockSummary.return_value = IrrigationActivateActuator(
            rainning=0,
            humidity=self.sensor_data.humidity,
            temperature=self.sensor_data.temperature,
        )

        self.strategy = SimpleActuatorIrirgationHandler()
        self.data_processor = SensorDataProcessor(
            stop_event=self.stop_event,
            observer=self.observer,
            pusblisher=self.pusblisher,
            actuator_strategy=self.strategy
        )

        self.data_processor._control_actuator_sensor_data()

        mock.assert_called_once_with(
            area=self.area
        )

    @patch.object(ServiceAreas, 'get_all')
    @patch.object(SensorDataProcessor, '_get_summary_sensor_data_area')
    @patch.object(SensorDataProcessor, '_handle_desactivate_actuator')
    def test_control_actuator_sensor_data_needs_to_desactivate_actuator_call_handler_once_ok(
            self, mock, mockSummary, mockAreas):
        self.sensor_data = SensorData(
            area_id=self.area.id,
            controller_id=1,
            area="name1",
            controller="name1",
            humidity=90,
            temperature=20,
            raining=True,
            date=datetime.datetime(2022, 7, 29, 21, 00, 00, 0)
        )

        self.stop_event = MagicMock()
        self.stop_event.is_set.side_effect = [
            False, True
        ]

        mockAreas.return_value = [
            self.area
        ]

        mockSummary.return_value = IrrigationActivateActuator(
            rainning=0,
            humidity=self.sensor_data.humidity,
            temperature=self.sensor_data.temperature,
        )

        self.strategy = SimpleActuatorIrirgationHandler()
        self.data_processor = SensorDataProcessor(
            stop_event=self.stop_event,
            observer=self.observer,
            pusblisher=self.pusblisher,
            actuator_strategy=self.strategy
        )

        self.data_processor.actuator_on = True

        self.data_processor._control_actuator_sensor_data()

        mock.assert_called_once_with(
            area=self.area
        )


if __name__ == '__main__':
    unittest.main()
