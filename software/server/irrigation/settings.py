"""
Settings files with variables used in the app
"""
from dotenv import load_dotenv, dotenv_values
# dotenv_values("/var/oee_services/.env") con esto funciona....
import os
from globals import TIMEOUT, BACKOFF_FACTOR, REINTENTOS, FORMAT_DATES


# load_dotenv()  # loading env variables

# loading env without altering the environment
if os.getenv('MODE') == 'test' and (os.getenv('INTEGRATION_TESTS', None) is not None):
    env = dotenv_values('.env_testing')
else:
    env = dotenv_values()

# To specify messages' topics => domain/messages/topics.py
# To specify observer events' topic => domain/observer/topics.py


# MODO
MODE = env.get('MODE', 'dev')

# API
API_HOST = env.get('API_HOST', '0.0.0.0')
API_PORT = int(env.get('API_PORT', 5000))

# DATABASES
print(env.get('DB_DATABASE_IRRIGATION'))
print(env.get('DB_DATABASE_IRRIGATION', 'irrigation'))


class DBMySQLSettings():
    HOST: str = env.get('DB_HOST', 'localhost')
    PORT: str = int(env.get('DB_PORT', 3306))
    USER: str = env.get('DB_USER', 'user')
    PASS: str = env.get('DB_PASS', 'shhhh it is a secret!')
    ROOT_PASS: str = env.get('DB_ROOT_PASS', 'shhhh it is a secret!')
    DATABASE: str = env.get('DB_DATABASE_IRRIGATION', 'irrigation')
    URI: str = env.get('DB_URI_IRRIGATION', 'sqlite://')


class DBMongoSettings():
    HOST: str = env.get('MONGODB_HOST', 'localhost')
    PORT: str = int(env.get('MONGODB_PORT', 3306))
    USER: str = env.get('MONGODB_USER', 'user')
    PASS: str = env.get('MONGODB_PASS', 'shhhh it is a secret!')
    DATABASE: str = env.get('MONGODB_DATABASE', 'irrigation')
    URI: str = env.get('MONGODB_URI', None)
    COLLECTION_SENSORS: str = 'sensors_historic'
    COLLECTION_ACTUATOR_IRRIGATION: str = 'irrigation_historic'


# MQTT
class MessagesSettings():
    HOST: str = env.get('MQTT_HOST', 'localhost')
    PORT: str = int(env.get('MQTT_PORT', '3306'))
    USER: str = env.get('MQTT_USER', 'user')
    PASS: str = env.get('MQTT_PASS', 'shhhh it is a secret!')


# settings classes
db_mysql_settings = DBMySQLSettings()
db_mongo_settings = DBMongoSettings()
messages_settings = MessagesSettings()
