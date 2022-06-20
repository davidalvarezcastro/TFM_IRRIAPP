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

SQL_CREATE_DATABASE = "CREATE DATABASE IF NOT EXISTS {database}"
SQL_GRANT_DATABASE = "GRANT ALL PRIVILEGES ON {database}.* TO {user}@\"%\""
SQL_INSERT_ADMIN = "INSERT INTO 'usuarios' ('username', 'password', 'nickname',\
    'nombre', 'apellido', 'email', 'es_admin', 'activo', 'salt') VALUES \
    (\"{username}\", \"{password}\", \"admin\", \"iav\", \"iav\", \"{email}\", 1, 1, \"{salt}\")"


@manager.command
def run():
    """Funcion para inciar la aplicación flask
    """
    init()


@manager.command
def db_init():
    """Función para iniciar la base de datos
    """
    base = "mysql \
        --user='{user}' --port={port} \
        --host='{host}' --password='{password}' ".format(
        user=db_settings.ROOT_USER,
        port=db_settings.PORT,
        host=db_settings.HOST,
        password=db_settings.ROOT_PASSWORD
    )

    # creamos la base de datos
    sql_crear = base + " -e '{sql}'".format(
        sql=SQL_CREATE_DATABASE.format(database=db_settings.DATABASE)
    )
    os.system(sql_crear)

    # privilegios sobre la base de datos
    sql_grant = base + " -e '{sql}'".format(
        sql=SQL_GRANT_DATABASE.format(
            user=db_settings.USER,
            database=db_settings.DATABASE
        )
    )
    os.system(sql_grant)

    # ejecutamos las migrations
    migrate()

    # insertamos el admin
    username = input('\tUsername (admin): ')
    password = input('\tPassword (admin): ')
    email = input('\tEmail (admin): ')
    salt = generate_salt()

    sql_admin_user = base + " --database='{database}' -e '{sql}'".format(
        database=db_settings.DATABASE,
        sql=SQL_INSERT_ADMIN.format(
            username=username,
            email=email,
            password=encode_password(password, salt),
            salt=salt
        )
    )
    os.system(sql_admin_user)


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
