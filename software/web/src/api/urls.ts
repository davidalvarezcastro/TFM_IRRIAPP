
/**
 * config
 */
export const BASE_URL = '/api/1.0/irrigation';

export const API_AREA_BASE = '/area'
export const API_AREAS_BASE = '/areas'
export const API_CONTROLLER_BASE = '/controller'
export const API_CONTROLLERS_BASE = '/controllers'

/**
 * endpoints
 */
export const API_AREA_TYPES_GET_ALL = `${BASE_URL}${API_AREA_BASE}/types`


export const API_AREAS_GET_ALL = `${BASE_URL}${API_AREAS_BASE}`
// export const API_AREAS_GET_AREA = `${BASE_URL}${API_AREA_BASE}/:area`
export const API_AREAS_POST = `${BASE_URL}${API_AREA_BASE}`
export const API_AREAS_PUT = `${BASE_URL}${API_AREA_BASE}/:area`
export const API_AREAS_DELETE = `${BASE_URL}${API_AREA_BASE}/:area`


export const API_CONTROLLERS_GET_ALL = `${BASE_URL}${API_CONTROLLERS_BASE}`
export const API_CONTROLLERS_GET_CONTROLLER = `${BASE_URL}${API_CONTROLLER_BASE}/:controller`
export const API_CONTROLLERS_POST = `${BASE_URL}${API_CONTROLLER_BASE}`
export const API_CONTROLLERS_PUT = `${BASE_URL}${API_CONTROLLER_BASE}/:controller`
export const API_CONTROLLERS_DELETE = `${BASE_URL}${API_CONTROLLER_BASE}/:controller`


export const API_SENSOR_DATA_HISTORICAL = `${BASE_URL}${API_CONTROLLER_BASE}/:controller/sensors/historical`
