import logging
import os
import sys


from utils.logs import Log

_LOGGER = Log(logger=logging.getLogger('irrigation'))


def logger_error(nombre: str = "", error: Exception = None) -> None:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    _LOGGER.error(
        '\n\n !!!!!! ERROR {} => {} \n\t type: {} \n\t filename: {} \n\t line: {} \n\n'.format(
            nombre, str(error),
            exc_type, fname, exc_tb.tb_lineno))
