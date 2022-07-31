import logging
import attr
import threading
import time
import queue

from utils import logger_error, get_now, Log
from patterns.pubsub import PubSubEvent, Sub
from domain.models.areas import Area
from domain.observer.topics import CONTROLLER_STATUS
from domain.models.controllers import Controller
from application.services.areas import ServiceAreas
from application.services.controllers import ServiceControllers
from application.services.sensor_data import ServiceSensorsHistoric
from domain.models.sensor_data_historic import SensorData
from domain.observer.controller_observer import ControllerEventsObserver
from microservices.data_collector.queue_status import QueueState


_LOGGER = Log(logger=logging.getLogger('irrigation'))


@attr.s
class SensorDataCollector(Sub):
    observer: ControllerEventsObserver = attr.ib()
    stop_event: threading.Event = attr.ib(default=threading.Event())

    # POST INIT HOOK
    def __attrs_post_init__(self):
        self._control_status_processing = {
            'thread': threading.Thread().start(),
            'event': threading.Event(),
            'active': False,
            'lock': threading.Lock(),
        }

        self.queue_status = queue.Queue()

        self._observer = self.observer
        self._observer.attach(self)

        self.service_sensor_data = ServiceSensorsHistoric()
        self.service_areas = ServiceAreas()
        self.service_controllers = ServiceControllers()

    # PATTERN METHODS
    def update(self, event: PubSubEvent) -> None:
        try:
            if event.type == CONTROLLER_STATUS:
                _LOGGER.debug(f"\t\tnew sensor status: {event}")
                topic = event.data.get('topic', None)
                payload = event.data.get('payload', None)

                # main goal is just to store events into a queue to be read asynchronously
                self.queue_status.put(
                    QueueState(
                        topic=topic,
                        payload=payload
                    )
                )

        except Exception as error:
            logger_error('update controller status message', error)
            raise error

    # METHODS
    def _init_control_status_processing_thread(self):
        thread_status_processing = threading.Thread(
            target=self._process_controller_status
        )
        thread_status_processing.daemon = True

        self._control_status_processing['thread'] = thread_status_processing
        self._control_status_processing['event'] = self.stop_event
        self._control_status_processing['active'] = True

        thread_status_processing.start()

    def _save_controller_state(self, data: QueueState):
        try:
            # recover area & controller info
            area_id = data.get_area()
            controller_id = data.get_controlller()
            payload = data.get_json()

            if area_id is None or controller_id is None:
                raise Exception(f"bad topic format: {data.topic}")

            area_info: Area = self.service_areas.get_by_id(
                area=area_id,
                all_visibility=True
            )
            controller_info: Controller = self.service_controllers.get_by_id(
                controller=controller_id,
                all_visibility=True
            )

            if controller_info.area != area_id:
                raise Exception(f"controler {controller_info} does not belong to area {area_id}")

            _LOGGER.debug("\tinserting data into mongodb... ")
            self.service_sensor_data.insert(
                data=SensorData(
                    area_id=area_id,
                    controller_id=controller_id,
                    area=area_info.name,
                    controller=controller_info.name,
                    humidity=payload.get('humidity', {}).get('value', -1),
                    temperature=payload.get('temperature', {}).get('value', -1),
                    raining=payload.get('raining', {}).get('value', 0),
                    date=get_now()
                )
            )
        except Exception as error:
            logger_error('_save_controller_state', error)
            raise error

    def _process_controller_status(self) -> None:
        try:
            while not self.stop_event.is_set():
                try:
                    new_state: QueueState = self.queue_status.get(block=False)
                    _LOGGER.debug(f"processing new sensor status: {new_state}")
                    self._save_controller_state(
                        data=new_state
                    )
                except queue.Empty:
                    pass
                time.sleep(1)
        except Exception as error:
            logger_error('_process_controller_status', error)
            raise error

    def run(self):
        self._init_control_status_processing_thread()
        self._control_status_processing['thread'].join()
