# -*- coding: utf-8 -*-
"""
    messages services tests
"""
import json
import os
import time
import unittest
import uuid

from unittest.mock import MagicMock, Mock, patch

from settings import messages_settings
from domain.messages.wrapper import MessagesClientWrapper
from domain.messages.services import MessagesInterface, MessagesServices
from domain.messages.topics import TOPIC_AREA_ACTUATOR_RELAY_OFF, TOPIC_AREA_ACTUATOR_RELAY_OFF_CONFIRMATION, TOPIC_AREA_ACTUATOR_RELAY_ON, TOPIC_AREA_ACTUATOR_RELAY_ON_CONFIRMATION, TOPIC_AREA_SENSORS_STATUS_CONTROLLER


os.environ['MODE'] = "test"


@unittest.skipUnless(os.getenv('UNIT_TESTS'), 'UNIT TEST')
class MessagesServicesUnitTest(unittest.TestCase):

    print('MessagesServicesUnitTest...')

    @patch('paho.mqtt.client.Client')
    def setUp(self, mockClient):
        self.area = 5
        self.controller = 2
        self.qos = 1
        self.wait_for_publish = False
        self.callback = lambda: True

        self.mock = MagicMock()
        self.mock.username_pw_set.return_value = Mock(return_value=None)
        self.mock.mock.connect.return_value = 8
        self.mock.loop_start.return_value = Mock(return_value=None)
        mockClient.return_value = self.mock

        self.client = MessagesClientWrapper(
            id="test",
            user=messages_settings.USER,
            password=messages_settings.PASS,
            host="localhost",
            port=5
        )

    # INNER METHODS

    # TESTS
    def test_raise_not_implementation_interface(self):
        class TestImplInterface(MessagesInterface):
            pass

        with self.assertRaises(Exception) as context:
            self.servicio = TestImplInterface()
        self.assertTrue(
            "Can't instantiate abstract class TestImplInterface with abstract methods"
            in str(context.exception))

        with self.assertRaises(Exception) as context:
            MessagesInterface.pub_sensors_status_controllers(self=self, area=1, controller=1)
        self.assertTrue(
            'NotImplementedException' in str(context.exception))

        with self.assertRaises(Exception) as context:
            MessagesInterface.pub_relay_on(self=self, area=1)
        self.assertTrue(
            'NotImplementedException' in str(context.exception))

        with self.assertRaises(Exception) as context:
            MessagesInterface.pub_relay_off(self=self, area=1)
        self.assertTrue(
            'NotImplementedException' in str(context.exception))

        with self.assertRaises(Exception) as context:
            MessagesInterface.sub_sensors_status_controllers(
                self=self, callback=None)

        with self.assertRaises(Exception) as context:
            MessagesInterface.sub_confirmation_relay_on(
                self=self, callback=None)

        with self.assertRaises(Exception) as context:
            MessagesInterface.sub_confirmation_relay_off(
                self=self, callback=None)
        self.assertTrue(
            'NotImplementedException' in str(context.exception))

    @patch.object(MessagesClientWrapper, 'pub', return_value=True)
    @patch.object(time, 'time', return_value=100)
    @patch.object(uuid, 'uuid4', return_value=100)
    def test_pub_sensor_status_function_is_called_ok(self, mockUuid, mockTime, mock):
        self.payload = {
            'id': uuid.uuid4(),
            'time': time.time()
        }

        self.service = MessagesServices(
            messages_client=self.client
        )

        self.service.pub_sensors_status_controllers(
            area=self.area,
            controller=self.controller,
            qos=self.qos,
            payload=self.payload,
            wait_for_publish=self.wait_for_publish,
        )

        mock.assert_called_once_with(
            topic=TOPIC_AREA_SENSORS_STATUS_CONTROLLER.format(
                area=self.area, controller=self.controller
            ),
            payload=json.dumps(self.payload),
            qos=self.qos,
            wait_for_publish=self.wait_for_publish,
        )

    @patch.object(MessagesClientWrapper, 'pub', return_value=True)
    def test_pub_relay_on_function_is_called_ok(self, mock):
        self.payload = {}

        self.service = MessagesServices(
            messages_client=self.client
        )

        self.service.pub_relay_on(
            area=self.area,
            qos=self.qos,
            payload=self.payload,
            wait_for_publish=self.wait_for_publish,
        )

        mock.assert_called_once_with(
            topic=TOPIC_AREA_ACTUATOR_RELAY_ON.format(
                area=self.area
            ),
            payload=json.dumps(self.payload),
            qos=self.qos,
            wait_for_publish=self.wait_for_publish,
        )

    @patch.object(MessagesClientWrapper, 'pub', return_value=True)
    def test_pub_relay_off_function_is_called_ok(self, mock):
        self.payload = {}

        self.service = MessagesServices(
            messages_client=self.client
        )

        self.service.pub_relay_off(
            area=self.area,
            qos=self.qos,
            payload=self.payload,
            wait_for_publish=self.wait_for_publish,
        )

        mock.assert_called_once_with(
            topic=TOPIC_AREA_ACTUATOR_RELAY_OFF.format(
                area=self.area
            ),
            payload=json.dumps(self.payload),
            qos=self.qos,
            wait_for_publish=self.wait_for_publish,
        )

    @patch.object(MessagesClientWrapper, 'sub', return_value=True)
    def test_sub_sensor_status_function_is_called_ok(self, mock):
        self.service = MessagesServices(
            messages_client=self.client
        )
        self.service.sub_sensors_status_controllers(
            callback=self.callback,
            qos=self.qos,
        )

        mock.assert_called_once_with(
            topic=TOPIC_AREA_SENSORS_STATUS_CONTROLLER.format(area="+", controller="+"),
            funcion=self.callback,
            qos=self.qos,
        )

    @patch.object(MessagesClientWrapper, 'sub', return_value=True)
    def test_sub_confirmation_relay_on_function_is_called_ok(self, mock):
        self.service = MessagesServices(
            messages_client=self.client
        )
        self.service.sub_confirmation_relay_on(
            callback=self.callback,
            qos=self.qos,
        )

        mock.assert_called_once_with(
            topic=TOPIC_AREA_ACTUATOR_RELAY_ON_CONFIRMATION.format(area="+"),
            funcion=self.callback,
            qos=self.qos,
        )

    @patch.object(MessagesClientWrapper, 'sub', return_value=True)
    def test_sub_confirmation_relay_off_function_is_called_ok(self, mock):
        self.service = MessagesServices(
            messages_client=self.client
        )
        self.service.sub_confirmation_relay_off(
            callback=self.callback,
            qos=self.qos,
        )

        mock.assert_called_once_with(
            topic=TOPIC_AREA_ACTUATOR_RELAY_OFF_CONFIRMATION.format(area="+"),
            funcion=self.callback,
            qos=self.qos,
        )


if __name__ == '__main__':
    unittest.main()
