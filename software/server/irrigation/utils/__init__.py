
from utils.logs import Log
from .dates import get_now, get_now_as_string
from .errors import logger_error

# init log handler
_LOGGER = Log(name="irrigation")
