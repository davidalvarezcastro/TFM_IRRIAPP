"""
    Service for getting message with the sensors status from the controllers
        - data getter thread
        - processing data thread
"""
import queue
import uuid


from settings import messages_settings
from domain.messages.wrapper import MessagesClientWrapper
from domain.messages.services import MessagesServices
from domain.observer.controller_observer import ControllerEventsObserver
from microservices.data_collector.data_collector import SensorDataCollector


class MicroserviceDataCollector():

    def _initialize_modules(self):
        # exceptions queue
        self.exceptions_queue = queue.Queue()

        # messages client
        self.message_client = MessagesClientWrapper(
            id="IRRIGATION_{}".format(uuid.uuid4()),
            user=messages_settings.USER,
            password=messages_settings.PASS,
            host=messages_settings.HOST,
            port=messages_settings.PORT
        )

        self.message_client.run()

        # messages interface
        self.message_service = MessagesServices(
            messages_client=self.message_client
        )

        # messages observer
        self.messages_manager = ControllerEventsObserver(
            queue=self.exceptions_queue,
            messages_service=self.message_service
        )
        self.messages_manager.init_subs()

        # initialize data collectot
        self.data_collector = SensorDataCollector(
            observer=self.messages_manager
        )

    def run(self):
        self._initialize_modules()
        self.data_collector.run()
