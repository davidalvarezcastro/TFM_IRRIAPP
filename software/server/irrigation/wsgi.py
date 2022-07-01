import logging

from utils import Log
from api.api import app


_LOGGER = Log(logger=logging.getLogger('irrigation'))
_LOGGER.info("Starting Irrigation Management System")
