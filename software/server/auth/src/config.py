# -*- coding: utf-8 -*-
""" Archivo con diferentes variables para el correcto funcionamiento de
la aplicación
"""
import os
from dotenv import load_dotenv

load_dotenv()


class ConfigDev:
    DEBUG = True
    TESTING = True


class ConfigProd:
    DEBUG = False
    TESTING = False


app_config = {
    'dev': ConfigDev,
    'prod': ConfigProd
}


class SettingsAPI:
    API_NAME: str = "Users Api"
    API_VERSION: str = "v1.0"
    API_PREFIX: str = f"/users/api/{API_VERSION}"

    API_HOST = '0.0.0.0'
    API_PORT = 5000
    API_SPEC_URL = '/doc'
    API_REST_TIMEOUT = 2
    API_REST_REINTENTOS = 3
    API_REST_BACKOFF_FACTOR = 0.3


class SettingsDatabase:
    HOST: str = os.getenv('DB_HOST', 'localhost')
    PORT: int = int(os.getenv('DB_PORT', 3306))
    USER: str = os.getenv('DB_USER', 'user')
    PASSWORD: str = os.getenv('DB_PASS', 'shhhh it is a secret!')
    ROOT_USER: str = os.getenv('DB_ROOT_USER', 'admin')
    ROOT_PASSWORD: str = os.getenv('DB_ROOT_PASS', 'shhhh it is also a secret!')
    DATABASE: str = os.getenv('DB_DATABASE_IRRIGATION', 'usuarios')
    USER_ADMIN_PASSWORD: str = os.getenv('USER_ADMIN_PASS', 'shhhh it is also a secret!')


api_settings = SettingsAPI()
db_settings = SettingsDatabase()
