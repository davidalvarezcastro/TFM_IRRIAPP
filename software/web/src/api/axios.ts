import { default as Axios } from 'axios';

interface ServerResponse {
  data: Record<string, unknown>
}

const API_URL = import.meta.env.VITE_API_URL as string;
const API_AUTH_URL = import.meta.env.VITE_API_AUTH_URL as string;

export const axios = Axios.create({
  baseURL: API_URL,
});

export const axios2 = Axios.create({
  baseURL: API_AUTH_URL,
});

axios.interceptors.response.use((response: ServerResponse) => {
  return response.data;
});

axios2.interceptors.response.use((response: ServerResponse) => {
  return response.data;
});



// Responses
export interface Response {
    status: string
}

export interface ErrorResponse {
    status: string,
    message: string,
}
