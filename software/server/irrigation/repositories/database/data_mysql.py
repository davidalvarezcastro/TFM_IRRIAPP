"""
    Init data database
"""

DATA_TYPES = [
    {'id': 1, 'description': 'irrigation control area'},
    {'id': 2, 'description': 'monitoring area'},
]

DATA_AREAS = [
    {'id': 1, 'name': 'test_area_davalv',
     'description': 'Simulation-testing area & general purpose tests for dev environment', 'visible': 0,
     'type': 1},
    {'id': 2, 'name': 'fresas_1_finca_torre',
     'description': 'Strawberries area outside the house and the main garden', 'visible': 1, 'type': 1}]

DATA_CONTROLLERS = [
    {'area': 1, 'id': 1, 'name': 'test_controller_simulator', 'key': None,
     'description': 'Simulation & testing controller for dev environment', 'visible': 0},
    {'area': 2, 'id': 2, 'name': 'meteo_sensors_controller', 'key': None,
     'description': 'Controller for reading meteological sensor data and send it to server', 'visible': 1}
]
