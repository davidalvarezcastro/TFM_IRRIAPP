"""
    Service for processing sensor data (historical) to resolve if it is necessary
    to activate or not the pertinent actuator (in this prototype, irrigation relay)
"""
import queue
import uuid


from settings import messages_settings
from domain.messages.wrapper import MessagesClientWrapper
from domain.messages.services import MessagesServices
from domain.observer.actuator_observer import ActuatorEventsObserver
from microservices.actuator_controller.data_processor import SensorDataProcessor
from application.actuator.models.simple_actuator_irrigation import SimpleActuatorIrirgationHandler


class MicroserviceHandleActuator():

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
        self.messages_manager = ActuatorEventsObserver(
            queue=self.exceptions_queue,
            messages_service=self.message_service
        )
        self.messages_manager.init_subs()

        self.actuator_activation_strategy = SimpleActuatorIrirgationHandler()

        # initialize data processing
        self.data_processor = SensorDataProcessor(
            observer=self.messages_manager,
            pusblisher=self.message_service,
            actuator_strategy=self.actuator_activation_strategy
        )

    def run(self):
        self._initialize_modules()
        self.data_processor.run()
