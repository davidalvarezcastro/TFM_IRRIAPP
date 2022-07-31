
/**
 * config
 */
export const BASE_URL_IRRIGATION = '/api/1.0/irrigation';
export const BASE_URL_AUTH = '/users/api/v1.0';

export const API_AREA_BASE = '/area'
export const API_AREAS_BASE = '/areas'
export const API_CONTROLLER_BASE = '/controller'
export const API_CONTROLLERS_BASE = '/controllers'

export const API_AUTH_BASE = '/auth'

/**
 * endpoints
 */
export const API_AREA_TYPES_GET_ALL = `${BASE_URL_IRRIGATION}${API_AREA_BASE}/types`


export const API_AREAS_GET_ALL = `${BASE_URL_IRRIGATION}${API_AREAS_BASE}`
export const API_AREAS_GET_AREA = `${BASE_URL_IRRIGATION}${API_AREA_BASE}/:area`
export const API_AREAS_POST = `${BASE_URL_IRRIGATION}${API_AREA_BASE}`
export const API_AREAS_PUT = `${BASE_URL_IRRIGATION}${API_AREA_BASE}/:area`
export const API_AREAS_DELETE = `${BASE_URL_IRRIGATION}${API_AREA_BASE}/:area`


export const API_CONTROLLERS_GET_ALL = `${BASE_URL_IRRIGATION}${API_CONTROLLERS_BASE}`
export const API_CONTROLLERS_GET_CONTROLLER = `${BASE_URL_IRRIGATION}${API_CONTROLLER_BASE}/:controller`
export const API_CONTROLLERS_POST = `${BASE_URL_IRRIGATION}${API_CONTROLLER_BASE}`
export const API_CONTROLLERS_PUT = `${BASE_URL_IRRIGATION}${API_CONTROLLER_BASE}/:controller`
export const API_CONTROLLERS_DELETE = `${BASE_URL_IRRIGATION}${API_CONTROLLER_BASE}/:controller`


export const API_SENSOR_DATA_HISTORICAL = `${BASE_URL_IRRIGATION}${API_CONTROLLER_BASE}/:controller/sensors/historical`

export const API_ACTUATOR_ACTIVATION_HISTORICAL = `${BASE_URL_IRRIGATION}${API_AREA_BASE}/:area/actuator/historical`


export const API_AUTH_LOGIN_POST = `${BASE_URL_AUTH}${API_AUTH_BASE}/login`
export const API_AUTH_LOGOUT_GET = `${BASE_URL_AUTH}${API_AUTH_BASE}/logout`
export const API_AUTH_REFRESH_TOKEN_GET = `${BASE_URL_AUTH}${API_AUTH_BASE}/refresh`
