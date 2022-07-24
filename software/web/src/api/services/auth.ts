import { User } from '../../types/auth';
import { axios2 } from '../axios';
import { API_AUTH_LOGIN_POST } from '../urls';


interface ResponseAuthLogin {
    token: string,
}

interface ResponseAuthLogout {
    msg: string,
}

export const postLogin = async (user: User): Promise<string> => {
    return axios2.post<any, ResponseAuthLogin>(API_AUTH_LOGIN_POST, user).then((data) => {
        if (data) {
            return data.token
        }

        return Promise.reject();
    })
}

export const getLogout = async (token: string): Promise<boolean> => {
    const headers = {
        'Authorization': token
    }

    return axios2.get<any, ResponseAuthLogout>(API_AUTH_LOGIN_POST, {
        headers: headers
    }).then((data) => {
        if (data) {
            return true;
        }

        return Promise.reject();
    })
}

export const getRefresh = async (token: string): Promise<string> => {
    const headers = {
        'Authorization': token
    }

    return axios2.get<any, ResponseAuthLogin>(API_AUTH_LOGIN_POST, {
        headers: headers
    }).then((data) => {
        if (data) {
            return data.token
        }

        return Promise.reject();
    })
}
