import { SensorData } from '../../types/sensor_data';
import { axios } from '../axios';
import { API_SENSOR_DATA_HISTORICAL } from '../urls';


interface ResponseSensorDataHistorical {
    data: {
        sensor_data: Record<string, string>[];
    };
    status: string,
}

export const getHistorical = async (startDate: string, endDate: string): Promise<SensorData[]> => {
    const queryParameters = `?start_date=${startDate}&end_date=${endDate}`;

    return axios.get<any, ResponseSensorDataHistorical>(`${API_SENSOR_DATA_HISTORICAL}${queryParameters}`).then((data) => {
        if (data) {
            return data.data.sensor_data.map(i => {
                return {
                    "controller": i.controller,
                    "controllerName": i.controller_name,
                    "area": i.area,
                    "areaName": i.area_name,
                    "humidity": i.humidity,
                    "temperature": i.temperature,
                    "raining": i.raining,
                    "date": i.date,
                } as unknown as SensorData
            });
        }

        return Promise.reject();
    })
}
