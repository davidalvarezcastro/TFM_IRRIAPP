"""
    Servicio encargado de recolectar los mensajes de estado de los diferentes controladores del sistema:
        - hilo recolector de estados
        - hilo para procesar los diferentes estados
"""
import queue
import uuid


from irrigation.domain.eventos.wrapper import WrapperEventos
from irrigation.domain.eventos.servicios import ServiciosEventos
from irrigation.domain.observer.gestor import GestorEventos
import irrigation.settings as settings


def _iniciar_recolector():

    # iniciamos el servicio de colisiones
    pass


if __name__ == '__main__':
    global cola_excepciones, servicio_eventos, gestor_eventos

    # cola de excepciones
    cola_excepciones = queue.Queue()

    # cliente coenxión eventos
    cliente_eventos = WrapperEventos(
        id="IRRIGATION_{}".format(uuid.uuid4()),
        user=settings.MQTT_BROKER_AUTH_USERNAME,
        password=settings.MQTT_BROKER_AUTH_PASSWORD,
        host=settings.MQTT_BROKER_IP,
        port=settings.MQTT_BROKER_PORT)

    cliente_eventos.iniciar()

    # interfaz de comunicación
    servicio_eventos = ServiciosEventos(
        cliente_eventos=cliente_eventos
    )

    # gestor de eventos (publisher)
    gestor_eventos = GestorEventos(
        queue=cola_excepciones,
        servicio_eventos=servicio_eventos
    )
    gestor_eventos.iniciar_subscriptores()
