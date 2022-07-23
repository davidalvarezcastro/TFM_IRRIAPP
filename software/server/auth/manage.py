# -*- coding: utf-8 -*-
"""
    script para la gestión de la api de auth desde la terminal
"""
import os
import unittest
import threading
from flask_script import Manager
import subprocess
import peeweedbevolve

from src.main import app, init
from src.config import db_settings
import src.model.model
from src.model.model import database as db
from src.util.authentication import encode_password, generate_salt


manager = Manager(app)


@manager.command
def run():
    """Funcion para inciar la aplicación flask
    """
    init()


@manager.command
def evolve():
    """Función para ejecutar la función evolve de la herramienta II de migraciones
    """
    db.evolve()


@manager.command
def generate_migrate():
    """Función para iniciar la base de datos
    """
    os.system("./venv/bin/pem watch")
    print("Revisa el directorio 'migrations' para renombrar y/o ver la lista\
de migraciones")


@manager.command
def migrate():
    """Función para iniciar la base de datos
    """
    os.system("./venv/bin/pem migrate")


@manager.command
def db_models():
    """Función para obtener los modelos de la base de datos

       NOTA: es necesario mover el archivo al directorio correspondiente
    """
    comando = "pwiz {database} -e mysql -u {user} -p {port} -H {host} -P".format(
        database=db_settings.DATABASE,
        user=db_settings.USER,
        port=db_settings.PORT,
        host=db_settings.HOST
    )
    os.system("./venv/bin/python -m {} >> models.py".format(comando))


if __name__ == '__main__':
    manager.run()
