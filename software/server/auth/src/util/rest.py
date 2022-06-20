# -*- coding: utf-8 -*-
"""Archivo con funcionalidades para peticiones rest
"""
import logging
import requests


class GestorPeticionesRest:
    """Clase para la gestión de peticiones rest"""
    _LOGGER = logging.getLogger(__name__)

    def __init__(self, timeout=3.5, reintentos=5, backoff_factor=0.3, auth=None, logs=False):
        self._timeout = timeout
        self._session = self.requests_retry_session(reintentos, backoff_factor)
        self._session.auth = auth
        if logs:
            self._session.hooks['response'].append(self.requests_logging)

    def __del__(self):
        self._session.close()

    @staticmethod
    def requests_retry_session(reintentos, backoff_factor):
        # Devuelve objeto requests.Session configurado para implementar
        # reintentos en caso de fallo en las peticiones HTTP
        session = requests.Session()
        retry = requests.packages.urllib3.util.retry.Retry(total=reintentos,
                                                           read=reintentos,
                                                           connect=reintentos,
                                                           backoff_factor=backoff_factor,
                                                           method_whitelist=False)
        adapter = requests.adapters.HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    @staticmethod
    def requests_logging(r, *args, **kwargs):
        logger = GestorPeticionesRest._LOGGER
        logger.debug('%s %s%s\n\tresponse: %s (HTTP %d)\n',
                     r.request.method,
                     r.url,
                     '\n\tdata: {}'.format(
                         r.request.body if r.request.body else ''),
                     r.content,
                     r.status_code)

    def _send(self, request):
        prep_request = self._session.prepare_request(request)
        try:
            r = self._session.send(prep_request, timeout=self._timeout)
            respuesta = r.content
        except requests.RequestException:
            self._LOGGER.error('[ERROR] %s %s\n%s', prep_request.method,
                               prep_request.url,
                               '\tdata: {}\n\n'.format(
                                   prep_request.body if prep_request.body else ''),
                               exc_info=True)
            print('\n\n\n\t[ERROR] %s %s\n%s', prep_request.method,
                               prep_request.url,
                               '\tdata: {}\n\n'.format(
                                   prep_request.body if prep_request.body else ''))
            respuesta = None
        return respuesta

    def get(self, url):
        request = requests.Request('GET', url)
        return self._send(request)

    def post(self, url, data):
        request = requests.Request('POST', url, json=data)
        return self._send(request)

    def put(self, url, data):
        request = requests.Request('PUT', url, json=data)
        return self._send(request)

    def delete(self, url):
        request = requests.Request('DELETE', url)
        return self._send(request)
