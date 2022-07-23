# -*- coding: utf-8 -*-
import logging
from microservices.data_collector.service import MicroserviceDataCollector

from utils import Log


_LOGGER = Log(logger=logging.getLogger('irrigation'))


if __name__ == '__main__':
    _LOGGER.info("Starting sensor data microservice...")
    service = MicroserviceDataCollector()
    service.run()
