""" Archivo con diferentes variables para el correcto funcionamiento de
la aplicación
"""
from dotenv import load_dotenv
import os


load_dotenv()  # cargamos las variables de entorno


# MODO
MODE = os.getenv('MODE', 'dev')


# DB
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = int(os.getenv('DB_PORT', '3306'))
DB_USER = os.getenv('DB_USER', 'user')
DB_ROOT_PASSWORD = os.getenv('DB_ROOT_PASS', 'shhhh it is a secret!')
DB_PASSWORD = os.getenv('DB_PASS', 'shhhh it is also a secret!')
DB_DATABASE = os.getenv('DB_DATABASE_IRRIGATION', 'irrigation')


# MONGODB
MONGODB_HOST = os.getenv('MONGODB_HOST', '172.17.0.1')
MONGODB_PORT = int(os.getenv('MONGODB_PORT_BINDED', 27017))
MONGODB_USER = os.getenv('MONGODB_USER', 'user')
MONGODB_PASSWORD = os.getenv('MONGODB_PASS', 'shhhh it is a secret!')
MONGODB_DATABASE = os.getenv('MONGODB_DATABASE', 'irrigation')


# API
API_HOST = os.getenv('API_HOST', '0.0.0.0')
API_PORT = int(os.getenv('API_PORT', '5000'))
API_VERSION = '1.0'
API_PREFIX = f"/api/{API_VERSION}/irrigation"

TIMEOUT = 2
REINTENTOS = 3
BACKOFF_FACTOR = 0.3


# OTHERS
FORMAT_DATES = "%Y-%m-%dT%H:%M:%SZ"


# MQTT
MQTT_BROKER_IP = os.getenv('SGE_HOST_LOCAL') if bool(int(os.getenv('MQTT_DOCKER'))) else \
    (os.getenv('SGE_HOST') if os.getenv(
        'SGE_HOST') is not None else '1.1.10.235')
MQTT_BROKER_PORT = int(os.getenv('SGE_PORT')) if bool(int(os.getenv('MQTT_DOCKER'))) else \
    (int(os.getenv('SGE_PORT_BINDED')) if os.getenv(
        'SGE_PORT_BINDED') is not None else 1884)
MQTT_BROKER_AUTH_USERNAME = os.getenv('SGE_USER') if os.getenv(
    'SGE_USER') is not None else 'username'
MQTT_BROKER_AUTH_PASSWORD = os.getenv('SGE_PASS') if os.getenv(
    'SGE_PASS') is not None else 'password'
