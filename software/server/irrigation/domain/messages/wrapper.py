# -*- coding: utf-8 -*-
import paho.mqtt.client
import threading
import time


class MessagesClientWrapper():
    """Clase para la gestión de conexiones al broker"""

    def __init__(self, id="", user="admin", password="admin", host="localhost", port=1883):
        """Inicializa instancia de la clase.

        Args:
            user (str): usuario para la conexión con el broker.
            password (str): contraseña del usuario.
            host (str): ip del servidor donde se encuentra el broker.
            port (int): puerto de conexión al broker.
        """
        self._id = id
        self._user = user
        self._password = password
        self._host = host
        self._port = port
        self.__will = None  # variable para almacenar el will en caso de no conexión
        self.__subs_list = []  # variable para almacenar la lista de subs en caso de no conexión

        self._retry_connection_manager = {
            'thread': threading.Thread().start(),
            'event': threading.Event(),
            'activo': False,
            'lock': threading.Lock(),
        }

        self.__setup_client()

        if self.__mqttclient is None:
            self._retry_mode()

    def __setup_client(self):
        """Configura un cliente MQTT y establece la comunicacion con el broker.

        Args:
            None
        """
        try:
            self.__mqttclient = paho.mqtt.client.Client(
                client_id=self._id,
                protocol=paho.mqtt.client.MQTTv311,
                transport='tcp',
                userdata={'controller': self})
            self.__mqttclient.username_pw_set(self._user, self._password)
        except Exception:
            self.__mqttclient = None

    def run(self):
        """Inicia el bucle de comunicación con el broker

        Importante: especificar last will antes de ejecutar esta función!

        Args:
            None
        """
        self.__mqttclient.connect(self._host, port=self._port)
        self.__mqttclient.loop_start()

    def _retry_mode(self):
        """Hilo para lanzar la comprobación de conexiones
        """
        stop_event = threading.Event()
        hilo_reintentos = threading.Thread(
            target=self._retry_mode_thread, args=(stop_event,))
        hilo_reintentos.daemon = True

        self._retry_connection_manager['thread'] = hilo_reintentos
        self._retry_connection_manager['event'] = stop_event
        self._retry_connection_manager['activo'] = True

        hilo_reintentos.start()

    def _retry_mode_thread(self, stop_event, forever=True):
        """Reintamos la conexión con el broker.

        Args:
            stop_event (threading.Event): flag para detener la ejecucion del
                hilo.
            forever(bool): indica si los reintentos son forevers. Por defecto
            a True.
        """
        reintentos = 1

        while self.__mqttclient is None:
            time.sleep(5)
            self._id = self._id + '_r' + str(reintentos)
            self.__setup_client()
            reintentos += 1

            if not forever:
                if reintentos > 10:
                    break
        if self.__will is not None:
            self.set_last_will(topic=self.__will['topic'],
                               payload=self.__will['payload'],
                               qos=self.__will['qos'])
        if len(self.__subs_list) > 0:
            for sub in self.__subs_list:
                self.sub(topic=sub['topic'],
                         funcion=sub['funcion'], qos=sub['qos'])

    def pub(self, topic, payload, qos=1, wait_for_publish=True, exception=True):
        """Función para publicar contenido a un topic específico

        Args:
            topic (str): topic
            payload (dict): contenido del mensaje
            qos (int): calidad del servicio
            wait_for_publish (bool): indica si esperamos a la respueta del broker
            exception (bool): raise Exception

        Returns:
            (Exception): devuelve una excepción en caso de fallo de conexión.
        """
        status = self.__mqttclient.publish(topic=topic, payload=payload, qos=1)
        if status.rc == paho.mqtt.client.MQTT_ERR_NO_CONN:
            if exception:
                raise Exception(paho.mqtt.client.error_string(status.rc))
        if wait_for_publish:
            status.wait_for_publish()

    def sub(self, topic, funcion, qos=1):
        """Función para subscribirse a un topic específico

        Args:
            topic (str): topic
            funcion (def): función que gestiona la llegada de mensajes del topic
            qos (int): calidad del servicio
        """
        try:
            # subscribe.callback(funcion, topic, qos=qos, hostname=self._host, auth={
            #     'username': self._user, 'password': self._password}, port=self._port, transport='tcp')
            self.__mqttclient.subscribe(topic)
            self.__mqttclient.message_callback_add(topic, funcion)
        except Exception:
            self.__subs_list.append({
                'topic': topic,
                'funcion': funcion,
                'qos': qos
            })

    def set_last_will(self, topic, payload, qos=2):
        """Configura el mensaje enviado en caso de desconexion con el servidor de eventos.

        Args:
            topic(str): topic al que subscribir el last will
            payload(str): payload del last will
            qos(int): quality of service
        """
        if self.__mqttclient is not None:
            self.__mqttclient.will_set(
                topic=topic,
                payload=payload,
                qos=qos)
        else:
            self.__will = {
                'topic': topic,
                'payload': payload,
                'qos': qos
            }
