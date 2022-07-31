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
from patterns import Pub, Sub, PubSubEvent
from domain.observer.topics import ACTUATOR_RELAY_ON_OK, ACTUATOR_RELAY_OFF_OK
from domain.observer.actuator_observer import ActuatorEventsObserver


os.environ['MODE'] = "test"


@unittest.skipUnless(os.getenv('UNIT_TESTS'), 'UNIT TEST')
class ActuatorObserverUnitTest(unittest.TestCase):

    print('ActuatorObserverUnitTest...')

    def setUp(self):
        self.queue = queue.Queue()
        self.messages_service = MagicMock()
        self.messages_service.sub_confirmation_relay_on.return_value = Mock(
            return_value=None)
        self.messages_service.sub_confirmation_relay_off.return_value = Mock(
            return_value=None)

        self.observer = ActuatorEventsObserver(
            queue=self.queue,
            messages_service=self.messages_service
        )

        self.topic = "topic"
        self.payload = {}
        self.msg = MQTTMessage(topic=self.topic.encode('utf-8'))
        self.msg.payload = json.dumps(self.payload)

    # INNER METHODS

    # TESTS
    def test_add_observer(self):
        class Observer(Sub):
            def __init__(self):
                self.updated = False
                self.event = None

            def update(self, event: PubSubEvent) -> None:
                self.updated = True
                self.event = event

        observer = Observer()
        self.assertEqual(len(self.observer._observers), 0)
        self.observer.attach(observer)
        self.assertEqual(len(self.observer._observers), 1)

    def test_delete_observer(self):
        class Observer(Sub):
            def __init__(self):
                self.updated = False
                self.event = None

            def update(self, event: PubSubEvent) -> None:
                self.updated = True
                self.event = event

        observer = Observer()
        self.assertEqual(len(self.observer._observers), 0)
        self.observer.attach(observer)
        self.assertEqual(len(self.observer._observers), 1)
        self.observer.detach(observer)
        self.assertEqual(len(self.observer._observers), 0)

    def test_notify_observer(self):
        type = "type"

        class Observer(Sub):
            def __init__(self):
                self.updated = False
                self.event = None

            def update(self, event: PubSubEvent) -> None:
                self.updated = True
                self.event = event

        observer = Observer()
        self.observer.attach(observer)

        self.assertEqual(len(self.observer._observers), 1)

        self.observer.notify(event=PubSubEvent(
            type=type,
            data=None
        ))

        self.assertTrue(observer.update)
        self.assertEqual(observer.event.type, type)

    @patch.object(ActuatorEventsObserver, 'notify', return_value=True)
    def test_notify_relay_on_confirmation_ok(self, mockNotify):
        self.observer._ActuatorEventsObserver__manage_relay_on_ok_status(
            None, None, self.msg)

        mockNotify.assert_called_once_with(event=PubSubEvent(
            type=ACTUATOR_RELAY_ON_OK,
            data={
                'topic': self.topic,
                'payload': json.dumps(self.payload)
            }
        ))
        self.assertTrue(self.queue.qsize() == 0)

    @patch.object(ActuatorEventsObserver, 'notify', return_value=True)
    def test_raise_exception_notify_observer_relay_on_ok(self, mockNotify):
        def side_effect(arg):
            raise Exception('asd')
        mockNotify.side_effect = side_effect

        self.observer._ActuatorEventsObserver__manage_relay_on_ok_status(
            None, None, self.msg)

        mockNotify.assert_called_once_with(event=PubSubEvent(
            type=ACTUATOR_RELAY_ON_OK,
            data={
                'topic': self.topic,
                'payload': json.dumps(self.payload)
            }
        ))
        self.assertTrue(self.queue.qsize() == 1)

    @patch.object(ActuatorEventsObserver, 'notify', return_value=True)
    def test_notify_relay_off_confirmation_ok(self, mockNotify):
        self.observer._ActuatorEventsObserver__manage_relay_off_ok_status(
            None, None, self.msg)

        mockNotify.assert_called_once_with(event=PubSubEvent(
            type=ACTUATOR_RELAY_OFF_OK,
            data={
                'topic': self.topic,
                'payload': json.dumps(self.payload)
            }
        ))
        self.assertTrue(self.queue.qsize() == 0)

    @patch.object(ActuatorEventsObserver, 'notify', return_value=True)
    def test_raise_exception_notify_observer_relay_off_ok(self, mockNotify):
        def side_effect(arg):
            raise Exception('asd')
        mockNotify.side_effect = side_effect

        self.observer._ActuatorEventsObserver__manage_relay_off_ok_status(
            None, None, self.msg)

        mockNotify.assert_called_once_with(event=PubSubEvent(
            type=ACTUATOR_RELAY_OFF_OK,
            data={
                'topic': self.topic,
                'payload': json.dumps(self.payload)
            }
        ))
        self.assertTrue(self.queue.qsize() == 1)

    def test_initialize_subscribers_ok(self):
        self.observer.init_subs()

        self.messages_service.sub_confirmation_relay_on.assert_called_once_with(
            callback=self.observer._ActuatorEventsObserver__manage_relay_on_ok_status
        )
        self.messages_service.sub_confirmation_relay_off.assert_called_once_with(
            callback=self.observer._ActuatorEventsObserver__manage_relay_off_ok_status
        )


if __name__ == '__main__':
    unittest.main()
