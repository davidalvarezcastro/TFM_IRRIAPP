import { Actuator } from '../../types/actuator';
import { axios } from '../axios';
import { API_ACTUATOR_ACTIVATION_HISTORICAL } from '../urls';


interface ResponseActuatorActivationHistorical {
    data: {
        actuator_activation: Record<string, string>[];
    };
    status: string,
}

export const getHistorical = async (area: number, startDate: string, endDate: string): Promise<Actuator[]> => {
    const queryParameters = `?start_date=${startDate}&end_date=${endDate}`;

    return axios.get<any, ResponseActuatorActivationHistorical>(`${API_ACTUATOR_ACTIVATION_HISTORICAL.replace(':area', area.toString())}${queryParameters}`).then((data) => {
        if (data) {
            return data.data.actuator_activation.map(i => {
                return {
                    "area": i.area,
                    "start_date": i.start_date,
                    "end_date": i.end_date,
                } as unknown as Actuator
            });
        }

        return Promise.reject();
    })
}
