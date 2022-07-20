import { Area } from '../../types/areas';
import { axios, ErrorResponse, Response } from '../axios';
import { API_AREAS_DELETE, API_AREAS_GET_ALL, API_AREAS_POST, API_AREAS_PUT } from '../urls';


interface ResponseGetAreas extends Response {
    data: {
        areas: Record<string, string>[];
    };
}

interface ResponsePPDArea extends Response {
    data: {
        area: number;
        msg: string;
    };
}


export const getAreas = async (allVisibility: boolean = false): Promise<Area[]> => {
    const queryParameters = `?all_visibility=${allVisibility}`;

    return axios.get<any, ResponseGetAreas>(`${API_AREAS_GET_ALL}${queryParameters}`).then((data) => {
        if (data) {
            return data.data.areas.map(i => {
                return {
                    id: parseInt(i.id),
                    name: i.name,
                    description: i.description,
                    type: parseInt(i.type),
                    visible: i.visible,
                    date: i.date,
                } as unknown as Area
            });
        }

        return Promise.reject();
    })
}

export const postArea = async (area: Area): Promise<number> => {
    return axios.post<any, ResponsePPDArea>(`${API_AREAS_POST.replace(':area', area.id.toString())}`, JSON.stringify(area)).then((data) => {
        if (data) {
            if (data.status === "error") {
                return Promise.reject(`Failed creating new area: ${(data as unknown as ErrorResponse).message}`);
            } else {
                return data.data.area;
            }
        }

        return Promise.reject();
    })
}

export const putArea = async (area: Area): Promise<boolean> => {
    return axios.post<any, ResponsePPDArea>(`${API_AREAS_PUT.replace(':area', area.id.toString())}`, JSON.stringify(area)).then((data) => {

        if (data) {
            if (data.status === "error") {
                return Promise.reject(`Failed updating area: ${(data as unknown as ErrorResponse).message}`);
            } else {
                return true;
            }
        }

        return Promise.reject();
    })
}

export const deleteArea = async (area: number): Promise<boolean> => {
    return axios.post<any, ResponsePPDArea>(`${API_AREAS_DELETE.replace(':area', area.toString())}`).then((data) => {

        if (data) {
            if (data.status === "error") {
                return Promise.reject(`Failed deleting area: ${(data as unknown as ErrorResponse).message}`);
            } else {
                return true;
            }
        }

        return Promise.reject();
    })
}
