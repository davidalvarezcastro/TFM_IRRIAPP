"""
    Service for getting message with the sensors state from the controllers
        - data getter thread
        - processing data thread
"""
import queue
import uuid


from irrigation.domain.messages.wrapper import MessagesClientWrapper
from irrigation.domain.messages.services import MessagesServices
from irrigation.domain.observer.manager import EventsManager
import irrigation.settings as settings


def init_data_getter():
    pass


if __name__ == '__main__':
    global exceptions_queue, message_service, messages_manager

    # exceptions queue
    exceptions_queue = queue.Queue()

    # messages client
    message_client = MessagesClientWrapper(
        id="IRRIGATION_{}".format(uuid.uuid4()),
        user=settings.MQTT_BROKER_AUTH_USERNAME,
        password=settings.MQTT_BROKER_AUTH_PASSWORD,
        host=settings.MQTT_BROKER_IP,
        port=settings.MQTT_BROKER_PORT)

    message_client.run()

    # interface
    message_service = MessagesServices(
        messages_client=message_client
    )

    # messages manager (publisher)
    messages_manager = EventsManager(
        queue=exceptions_queue,
        messages_service=message_service
    )
    messages_manager.init_subs()
