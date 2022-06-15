"""
    Simulador que permite emitir eventos continuos simulando el comportamiento de un controlador
"""
import uuid


from irrigation.domain.eventos.wrapper import WrapperEventos
from irrigation.domain.eventos.servicios import ServiciosEventos
import irrigation.settings as settings


if __name__ == '__main__':
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

    while True:
        servicio_eventos.pub_estado_sensores_controladores(
            zona='test',
            controlador='test'
        )
