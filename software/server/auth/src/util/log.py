"""Archivo con las utilidades generales de la aplicación
"""
import logging
from logging.handlers import RotatingFileHandler
import os

LOGFILE_SIZE = 5 # mb


class Log(object):
    """ Clase para la gestión de logs
    """

    logger = None
    c_handler = None
    f_handler = None

    def __init__(self, filename="cf.log", logger=None):
        if logger is None:
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(logging.DEBUG)

            self.c_handler = logging.StreamHandler()

            try:
                self.f_handler = logging.handlers.RotatingFileHandler(
                    filename, maxBytes=LOGFILE_SIZE * (2 ** 20), backupCount=3)
            except Exception:
                path = os.path.dirname(filename)
                if not os.path.exists(path):
                    os.makedirs(path)
                self.f_handler = logging.handlers.RotatingFileHandler(
                    filename, maxBytes=LOGFILE_SIZE * (2 ** 20), backupCount=3)

            c_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            self.c_handler.setFormatter(c_format)
            self.f_handler.setFormatter(f_format)

            self.c_handler.setLevel(logging.DEBUG)
            self.f_handler.setLevel(logging.DEBUG)


            self.logger.addHandler(self.c_handler) # stdout terminal
            self.logger.addHandler(self.f_handler)
        else:
            self.logger = logger

    def debug(self, msg):
        self.logger.debug(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)