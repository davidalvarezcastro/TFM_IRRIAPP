from secrets import AREA_ACTUATOR

# pinouts
PINOUT_RELAY = 5

# mqtt
AREA_ID = f"area-{AREA_ACTUATOR}-actuator-relay"

TOPIC_TURN_ON = "area/{area}/actuator/on"
TOPIC_CONFIRMATION_TURN_ON = "area/{area}/actuator/on/ok"
TOPIC_TURN_OFF = "area/{area}/actuator/off"
TOPIC_CONFIRMATION_TURN_OFF = "area/{area}/actuator/off/ok"

# API_HOST = "0.0.0.0"
# API_PORT = 80

# API_TURN_ON = '/api/relay/on'
# API_TURN_OFF = '/api/relay/off'
