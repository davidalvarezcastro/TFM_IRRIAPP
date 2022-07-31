# -*- coding: utf-8 -*-
import logging
from microservices.actuator_controller.service import MicroserviceHandleActuator

from utils import Log


_LOGGER = Log(logger=logging.getLogger('irrigation'))


if __name__ == '__main__':
    _LOGGER.info("Starting actuator handler microservice...")
    service = MicroserviceHandleActuator()
    service.run()
