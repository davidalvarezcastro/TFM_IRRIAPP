import logging
import attr
import datetime
import threading
import time
import queue

from utils import logger_error, get_now
from globals import AREA_ACTUATOR_IRRIGATION
from utils.logs import Log
from patterns.pubsub import PubSubEvent, Sub
from domain.models.areas import Area
from domain.observer.topics import ACTUATOR_RELAY_ON_OK, ACTUATOR_RELAY_OFF_OK
from domain.messages.services import MessagesServices
from application.services.areas import ServiceAreas
from domain.models.irrigation_data import IrrigationData
from application.services.controllers import ServiceControllers
from application.services.sensor_data import ServiceSensorsHistoric
from domain.models.sensor_data_historic import QuerySensorData
from domain.observer.controller_observer import ControllerEventsObserver
from application.services.irrigation_data import ServiceIrrigationHistoric
from domain.models.irrigation_actuator_algorithm import IrrigationActivateActuator
from microservices.actuator_controller.settings import DATA_PROCESSING_ACTUATOR_TIMER
from microservices.actuator_controller.queue_status import QueueState
from application.actuator.models.interface_actuator_irrigation import InterfaceActuatorIrirgationHandler


_LOGGER = Log(logger=logging.getLogger('irrigation'))


@attr.s
class SensorDataProcessor(Sub):
    observer: ControllerEventsObserver = attr.ib()
    pusblisher: MessagesServices = attr.ib()
    # strategy pattern to determinate actuator activation algorithm
    actuator_strategy: InterfaceActuatorIrirgationHandler = attr.ib()
    stop_event: threading.Event = attr.ib(default=threading.Event())

    # POST INIT HOOK
    def __attrs_post_init__(self):
        self._control_sensor_data_processing_actuator = {
            'thread': threading.Thread().start(),
            'event': threading.Event(),
            'active': False,
            'lock': threading.Lock(),
        }

        self.queue_confirmations = queue.Queue()  # needed to communicate threads

        self._observer = self.observer
        self._observer.attach(self)

        self.service_sensor_data = ServiceSensorsHistoric()
        self.service_irrigation = ServiceIrrigationHistoric()
        self.service_areas = ServiceAreas()
        self.service_controllers = ServiceControllers()

        self.actuator_on = False  # maybe it is a better idea to get this value using irrigation mongo?

    # PATTERN METHODS
    def update(self, event: PubSubEvent) -> None:
        try:
            if event.type == ACTUATOR_RELAY_ON_OK or event.type == ACTUATOR_RELAY_OFF_OK:
                _LOGGER.debug(f"\t\t new confirmation from actuator: {event} ")
                topic = event.data.get('topic', None)
                payload = event.data.get('payload', None)

                # main goal is just to store events into a queue to be read asynchronously
                self.queue_confirmations.put(
                    QueueState(
                        type=event.type,
                        topic=topic,
                        payload=payload
                    )
                )
        except Exception as error:
            logger_error('update controller status message', error)
            raise error

    # METHODS
    def _init_sensor_data_processing_actuator(self):
        thread_sensor_data_processing = threading.Thread(
            target=self._control_actuator_sensor_data
        )
        thread_sensor_data_processing.daemon = True

        self._control_sensor_data_processing_actuator['thread'] = thread_sensor_data_processing
        self._control_sensor_data_processing_actuator['event'] = self.stop_event
        self._control_sensor_data_processing_actuator['active'] = True

        thread_sensor_data_processing.start()

    def _get_summary_sensor_data_area(self, area: Area) -> IrrigationActivateActuator:
        last_sensor_data = []
        result = None

        try:
            # get all controllers from area
            controllers = self.service_controllers.get_by_area(
                area=area.id,
                all_visibility=True
            )

            if len(controllers) <= 0:
                return None

            # last value stored (from all controllers)
            for controller in controllers:

                # last value controller
                result = self.service_sensor_data.get_last(
                    query=QuerySensorData(
                        area_id=area.id,
                        controller_id=controller.id,
                    )
                )

                if result is not None:
                    last_sensor_data.append(result)

            # get data from last 24 hours (one controller is enough to check it)
            end_last_value = get_now()
            start_last_value = get_now() - datetime.timedelta(hours=24)

            result = self.service_sensor_data.get(
                query=QuerySensorData(
                    area_id=area.id,
                    controller_id=controllers[0].id,
                    start_date=start_last_value,
                    end_date=end_last_value,
                )
            )

            # average values
            number_controllers = len(last_sensor_data)
            if number_controllers > 0:
                average_temperature = (
                    sum(list(map(lambda data: data.temperature, last_sensor_data)))) / number_controllers
                average_humidity = (
                    sum(list(map(lambda data: data.humidity, last_sensor_data)))) / number_controllers
            else:
                average_temperature = 0
                average_humidity = 0

            # % of the last 24 hours it was raining
            entries_rainning_last_24_hours = len(result)
            if entries_rainning_last_24_hours > 0:
                average_rainning_last_24_hours = (
                    sum(list(map(lambda data: data.raining, result)))) / entries_rainning_last_24_hours * 100
            else:
                average_rainning_last_24_hours = 0

            result = IrrigationActivateActuator(
                rainning=round(average_rainning_last_24_hours, 2),
                humidity=average_humidity,
                temperature=average_temperature,
            )
        except Exception as error:
            logger_error('_get_summary_sensor_data_area', error)

        return result

    def _wait_for_confirmation_from_actuator(self, area: int, mode_on: bool):
        max_retries = 3
        result = False

        while not max_retries <= 0:
            max_retries -= 1

            try:
                new_state: QueueState = self.queue_confirmations.get(block=False)
                _LOGGER.debug(f"\nprocessing new confirmation evento from the  actuator: \n\t\t{new_state}\n")
                result = new_state.get_type() == (ACTUATOR_RELAY_ON_OK if mode_on else ACTUATOR_RELAY_OFF_OK)
                if result:
                    break
            except queue.Empty:
                pass

            time.sleep(0.5)
        return result

    def _handle_activate_actuator(self, area: Area) -> bool:
        # communicate with actuator by using mqtt
        self.pusblisher.pub_relay_on(
            area=area.id,
            payload={}
        )

        actuator_on = self._wait_for_confirmation_from_actuator(
            area=area,
            mode_on=True
        )

        _LOGGER.debug(f"\t\t activate actuator? {actuator_on} ")

        # insert data mongo
        if actuator_on:
            _LOGGER.debug(f"\t\t inserting new entry into irrigation database for area {area.id} ")
            self.service_irrigation.insert(
                data=IrrigationData(
                    area_id=area.id,
                    area=area.name,
                    irrigation=actuator_on,
                    start_date=get_now(),
                    end_date=''  # mark as watering
                )
            )

        return actuator_on

    def _handle_desactivate_actuator(self, area: Area) -> bool:
        self.pusblisher.pub_relay_off(
            area=area.id,
            payload={}
        )
        actuator_off = self._wait_for_confirmation_from_actuator(
            area=area,
            mode_on=False
        )

        _LOGGER.debug(f"\t\t desactivate actuator? {actuator_off} ")

        # update data mongo
        if actuator_off:
            _LOGGER.debug(f"\t\t end irrigation for area {area.id} ")
            self.service_irrigation.end_irrigation(
                area=area.id
            )

        return actuator_off

    def _control_actuator_sensor_data(self) -> None:
        try:
            while not self.stop_event.is_set():
                _LOGGER.debug("check actuator activation conditions...")
                areas = self.service_areas.get_all(
                    all_visibility=True
                )

                for area in areas:

                    # check area type
                    if area.type != AREA_ACTUATOR_IRRIGATION:
                        continue

                    # get summary info about sensor data (from all controllers)
                    data_check_activate_actuator = self._get_summary_sensor_data_area(
                        area=area
                    )

                    # do we need to activate the relay?
                    activate_actuator = self.actuator_strategy.check_activate_irrigation(
                        query=data_check_activate_actuator
                    )
                    _LOGGER.debug(
                        f"\nbase conditions: {data_check_activate_actuator}\n\t activate? {activate_actuator}")

                    if activate_actuator and not self.actuator_on:
                        self.actuator_on = self._handle_activate_actuator(
                            area=area
                        )

                    if not activate_actuator and self.actuator_on:
                        self.actuator_on = not self._handle_desactivate_actuator(
                            area=area
                        )

                time.sleep(DATA_PROCESSING_ACTUATOR_TIMER)
        except Exception as error:
            logger_error('_control_actuator_sensor_data', error)
            raise error

    def run(self):
        self._init_sensor_data_processing_actuator()
        self._control_sensor_data_processing_actuator['thread'].join()
