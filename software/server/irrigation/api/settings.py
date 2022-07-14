# -*- coding: utf-8 -*-

API_VERSION = '1.0'
API_PREFIX = f"/api/{API_VERSION}/irrigation"

MIMETYPE_JSON = 'application/json'


# endpoints
API_AREA_TYPES = "/area/type"

API_GET_ALL_AREA_TYPES = "/area/types"
API_AREA_AREAS = "/area"
API_GET_ALL_AREAS = "/areas"

API_AREA_CONTROLLERS = "/controller"
API_GET_ALL_CONTROLLERS = "/controllers"

API_GET_HISTORIC_SENSOR_DATA_CONTROLLER = "/controller/{controller}/sensors/historical"
