"""
    Script for testing app outside a docker container

    NOTE: be careful!!
"""
# -*- coding: utf-8 -*-
import logging

from utils import Log
from api.api import app
from settings import API_HOST, API_PORT


_LOGGER = Log(logger=logging.getLogger('irrigation'))


if __name__ == '__main__':
    _LOGGER.info("Starting irrigation management system")
    # run
    app.run(host=API_HOST, port=API_PORT)
