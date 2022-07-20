import CryptoJS from 'crypto-js';
import jwt from 'jsonwebtoken';
import {
    setSession,
    getInfoSession,
    clearSession
} from '@/services/auth/session';
import {
    ACCESS_TOKEN,
    EXPIRES_AT,
    ID_TOKEN
} from '@/services/auth/session';

import { 
    postLoginAPI
} from "sal-js-lib/lib/api/usuarios";

// Módulo login
const login = {
    namespaced: true,
    state: {
        status: '',
        idToken: getInfoSession(ID_TOKEN),
        token: getInfoSession(ACCESS_TOKEN),
        expiration: getInfoSession(EXPIRES_AT),
        user: null

    },

    getters: {
        isLoggedIn: state => !!state.token,
        token: state => state.token,
        isValidSession: state => {
            try {
                if (state.idToken != null && state.token != null && state.expiration != null && new Date().getTime() < JSON.parse(state.expiration)) {
                    jwt.verify(state.token, process.env.VUE_APP_SECRET_TOKEN);
                    return true
                } else {
                    return false;
                }
            } catch (err) {
                console.log(err)
                return false
            }
        },
        userNameToken: state => {
            try {
                let info = jwt.verify(state.token, process.env.VUE_APP_SECRET_TOKEN);
                return info.username;
            } catch (error) {
                return '';
            }
        },
        authStatus: state => state.status,
    },

    mutations: {
        SET_AUTH_REQUEST: (state) => {
            state.status = 'loading'
        },

        SET_AUTH_SUCCESS: (state, {
            idToken,
            accessToken,
            expiresIn,
            user
        }) => {
            state.idToken = idToken
            state.token = accessToken
            state.expiration = expiresIn
            state.user = user
        },

        SET_AUTH_ERROR: (state) => {
            state.status = 'error';
        },

        SET_LOGOUT: (state) => {
            state.status = '';
            state.idToken = null;
            state.token = null;
            state.expiration = null;
        }
    },

    actions: {
        /**
         * Acción cuando realizamos el login del usuario
         */
        loginACTION: async ({ commit }, user) => {
            try {
                let info = await postLoginAPI(user.email, user.password)

                const idToken = process.env.BASE_URL + CryptoJS.AES.encrypt(user.username, "david") + '_' + (new Date()).toISOString().slice(0, 10).replace(/-/g, "");
                let token = jwt.verify(info.token, process.env.VUE_APP_SECRET_TOKEN);

                if (!token.admin) {
                    throw "El usuario no es un administrdor! Acceso restringido!";
                }

                let sesion = {
                    idToken: idToken,
                    accessToken: info.token,
                    expiresIn: token.exp,
                }

                setSession(sesion)
                sesion.user = user;
                commit('SET_AUTH_SUCCESS', sesion)
                console.log("Login: ok!")
            } catch (error) {
                commit('SET_AUTH_ERROR')
                clearSession();
                console.log(`Credenciales incorrectas!`, error)
                throw error;
            }
        },

        /**
         * Acción cuando realizamos el logout del usuario
         */
        logoutACTION: ({
            commit
        }) => {
            clearSession()
            commit('SET_LOGOUT')
            console.log(`Logout: ok!`)
        },
    },
};

export default login;