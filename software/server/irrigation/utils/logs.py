# -*- coding: utf-8 -*-
"""Clase wrapper para la gestión de logs de la aplicación
"""
import logging
from logging.handlers import RotatingFileHandler
import os
import irrigation.settings as settings

LOG_FORMAT_STR = '[%(asctime)s] %(levelname)s - %(message)s'
LOGFILE = f"/logs/irrigation_{settings.MODE}.log"
LOGFILE_SIZE = 5  # mb


class Log(object):
    """ Clase para la gestión de Logs
    """

    def __init__(self, filename=LOGFILE, name=__name__, logger=None):
        """Inicializamos la configuración del Logs

        Args:
            filename(str): ruta del archivo de logs resultante
            logger(logging.logger): logger
        """
        if logger is None:
            self.logger = logging.getLogger(name=name)
            self.logger.setLevel(logging.DEBUG)

            c_handler = logging.StreamHandler()
            try:
                f_handler = logging.handlers.RotatingFileHandler(
                    filename, maxBytes=LOGFILE_SIZE * (2 ** 20), backupCount=3)
            except Exception:
                f_handler = logging.handlers.RotatingFileHandler(
                    os.path.expanduser("~") + '/' + filename,
                    maxBytes=LOGFILE_SIZE * (2 ** 20), backupCount=3)

            c_format = logging.Formatter(LOG_FORMAT_STR)
            f_format = logging.Formatter(LOG_FORMAT_STR)
            c_handler.setFormatter(c_format)
            f_handler.setFormatter(f_format)

            self.logger.addHandler(c_handler)  # stdout terminal
            self.logger.addHandler(f_handler)
        else:
            self.logger = logger

    def info(self, msg):
        self.logger.info(msg)

    def debug(self, msg):
        self.logger.debug(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)
