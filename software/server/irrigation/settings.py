"""
Settings files with variables used in the app
"""
from dotenv import load_dotenv
import os


load_dotenv()  # loading env variables


# MODO
MODE = os.getenv('MODE', 'dev')


# DB
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = int(os.getenv('DB_PORT', 3306))
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
API_PORT = int(os.getenv('API_PORT', 5000))


TIMEOUT = 2
REINTENTOS = 3
BACKOFF_FACTOR = 0.3


# OTHERS
FORMAT_DATES = "%Y-%m-%dT%H:%M:%SZ"


# MQTT
MQTT_BROKER_IP = os.getenv('MQTT_HOST', 'localhost')
MQTT_BROKER_PORT = int(os.getenv('MQTT_PORT', '3306'))
MQTT_BROKER_AUTH_USERNAME = os.getenv('MQTT_USER', 'user')
MQTT_BROKER_AUTH_PASSWORD = os.getenv('MQTT_PASS', 'shhhh it is a secret!')
