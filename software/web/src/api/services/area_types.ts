import { AreaType } from '../../types/area_types';
import { axios } from '../axios';
import { API_AREA_TYPES_GET_ALL } from '../urls';


interface ResponseAreaTypes {
    data: {
        types: Record<string, string>[];
    };
    status: string,
}

export const getAreaTypes = async (): Promise<AreaType[]> => {
    return axios.get<any, ResponseAreaTypes>(API_AREA_TYPES_GET_ALL).then((data) => {
        if (data) {
            return data.data.types.map(i => {
                return {
                    "id": parseInt(i.id),
                    "description": i.description,
                } as unknown as AreaType
            });
        }

        return Promise.reject();
    })
}
