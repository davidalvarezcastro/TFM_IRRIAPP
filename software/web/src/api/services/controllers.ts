import { Controller } from '../../types/controllers';
import { axios, ErrorResponse, Response } from '../axios';
import { API_CONTROLLERS_DELETE, API_CONTROLLERS_GET_ALL, API_CONTROLLERS_POST, API_CONTROLLERS_PUT } from '../urls';


interface ResponseGetControllers extends Response {
    data: {
        controllers: Record<string, string>[];
    };
}

interface ResponsePPDController extends Response {
    data: {
        controller: number;
        msg: string;
    };
}


export const getControllers = async (allVisibility: boolean = false): Promise<Controller[]> => {
    const queryParameters = `?all_visibility=${allVisibility}`;

    return axios.get<any, ResponseGetControllers>(`${API_CONTROLLERS_GET_ALL}${queryParameters}`).then((data) => {
        if (data) {
            return data.data.controllers.map(i => {
                return {
                    id: parseInt(i.id),
                    area: parseInt(i.area),
                    name: i.name,
                    description: i.description,
                    type: parseInt(i.id),
                    visible: i.visible,
                    date: i.date,
                } as unknown as Controller
            });
        }

        return Promise.reject();
    })
}

export const postController = async (controller: Controller): Promise<number> => {
    return axios.post<any, ResponsePPDController>(`${API_CONTROLLERS_POST}`, controller).then((data) => {
        if (data) {
            if (data.status === "error") {
                return Promise.reject(`Failed creating new controller: ${(data as unknown as ErrorResponse).message}`);
            } else {
                return data.data.controller;
            }
        }

        return Promise.reject();
    })
}

export const putController = async (controller: number, info: Controller): Promise<boolean> => {
    return axios.put<any, ResponsePPDController>(`${API_CONTROLLERS_PUT.replace(':controller', controller.toString())}`, info).then((data) => {

        if (data) {
            if (data.status === "error") {
                return Promise.reject(`Failed updating controller: ${(data as unknown as ErrorResponse).message}`);
            } else {
                return true;
            }
        }

        return Promise.reject();
    })
}

export const deleteController = async (controller: number): Promise<boolean> => {
    return axios.delete<any, ResponsePPDController>(`${API_CONTROLLERS_DELETE.replace(':controller', controller.toString())}`).then((data) => {

        if (data) {
            if (data.status === "error") {
                return Promise.reject(`Failed deleting controller: ${(data as unknown as ErrorResponse).message}`);
            } else {
                return true;
            }
        }

        return Promise.reject();
    })
}
