import CryptoJS from 'crypto-js';
import jwt_decode from 'jwt-decode';
import {
    ACTION_LOGIN,
    ACTION_LOGOUT,
    GETTER_AUTH_TOKEN,
    GETTER_AUTH_TOKEN_ADMIN,
    GETTER_AUTH_TOKEN_INFO,
    GETTER_AUTH_TOKEN_USER,
    GETTER_AUTH_VALID_SESSION,
    MUTATION_SET_AUTH_ERROR,
    MUTATION_SET_AUTH_REQUEST,
    MUTATION_SET_AUTH_SUCCESS,
    MUTATION_SET_LOGOUT,
} from "./variables";
import { Session, User } from "../types/auth";
import { ACCESS_TOKEN, clearSession, EXPIRES_AT, getInfoSession, ID_TOKEN, setSession } from "../services/auth/session";
import { postLogin } from '../api/services/auth';

export interface AuthState {
    status: string,
    idToken: string,
    token: string,
    expiration: string,
    user: User | null
}

const initialState = {
    status: '',
    idToken: getInfoSession(ID_TOKEN),
    token: getInfoSession(ACCESS_TOKEN),
    expiration: getInfoSession(EXPIRES_AT),
    user: null
} as AuthState;

const auth = {
    namespaced: true,
    state: initialState,

    getters: {
        [GETTER_AUTH_TOKEN]: (state: AuthState): string => state.token,
        [GETTER_AUTH_VALID_SESSION]: (state: AuthState): boolean => {
            try {
                if (state.idToken !== '' && state.token !== '' && state.expiration !== '' && new Date().getTime() < JSON.parse(state.expiration)) {
                    return true
                } else {
                    return false;
                }
            } catch (err) {
                if (import.meta.env.NODE_ENV !== 'production') console.log(err)
                return false
            }
        },
        [GETTER_AUTH_TOKEN_INFO]: (state: AuthState): Record<string, string> => {
            try {
                return jwt_decode(state.token) as Record<string, string>;
            } catch (error) {
                return {};
            }
        },
        [GETTER_AUTH_TOKEN_USER]: (state: AuthState, getters: Record<string, Record<string, string>>): string => {
            try {
                return getters[GETTER_AUTH_TOKEN_INFO].username
            } catch (error) {
                return '';
            }
        },
        [GETTER_AUTH_TOKEN_ADMIN]: (state: AuthState, getters: Record<string, Record<string, boolean>>): boolean => {
            try {
                console.log(getters[GETTER_AUTH_TOKEN_INFO])
                return getters[GETTER_AUTH_TOKEN_INFO].admin
            } catch (error) {
                return false;
            }
        },
    },

    mutations: {
        [MUTATION_SET_AUTH_REQUEST]: (state: AuthState) => {
            state.status = 'loading'
        },

        [MUTATION_SET_AUTH_SUCCESS]: (state: AuthState, {
            idToken,
            accessToken,
            expiresAt,
            user
        }: Session) => {
            state.idToken = idToken
            state.token = accessToken
            state.expiration = expiresAt
            state.user = user as User
        },

        [MUTATION_SET_AUTH_ERROR]: (state: AuthState) => {
            state.status = 'error';
        },

        [MUTATION_SET_LOGOUT]: (state: AuthState) => {
            state.status = '';
            state.idToken = '';
            state.token = '';
            state.expiration = '';
        }
    },

    actions: {
        /**
         * Handle login action in the app
         */
        [ACTION_LOGIN]: async ({ commit }: {
            commit: <T extends unknown[]>(...args: T) => void;
        }, user: User) => {
            try {
                let jwtToken = await postLogin(user)
                const idToken = CryptoJS.AES.encrypt(user.user, "irriapp") + '_' + (new Date()).toISOString().slice(0, 10).replace(/-/g, "");

                let token = jwt_decode(jwtToken) as Record<string, string>
                // if (!token.admin) {
                //     throw "Not admin user! Forbidden access!";
                // }

                let sesion = {
                    idToken: idToken,
                    accessToken: jwtToken,
                    expiresAt: token.exp,
                } as Session

                setSession(sesion)
                sesion.user = user;
                commit(MUTATION_SET_AUTH_SUCCESS, sesion)
                if (import.meta.env.NODE_ENV !== 'production') console.log("Login: ok!")
            } catch (error) {
                commit(MUTATION_SET_AUTH_ERROR)
                clearSession();
                if (import.meta.env.NODE_ENV !== 'production') console.log(`Bad credentials!`, error)
                // @ts-ignore
                throw error.response.data.message;
            }
        },

        /**
         * Handle logout action in the app
         */
        [ACTION_LOGOUT]: ({
            commit
        }: {
            commit: <T extends unknown[]>(...args: T) => void;
        }) => {
            clearSession()
            commit(MUTATION_SET_LOGOUT)
            if (import.meta.env.NODE_ENV !== 'production') console.log(`Logout: ok!`)
        },
    },
};

export default auth;
