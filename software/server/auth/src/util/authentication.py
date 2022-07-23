import os
import jwt
import hashlib
from datetime import datetime, timedelta
from flask import request
from functools import wraps

from src.dto.dto import DTOError
from src.dao.user import DAOUser
from src.model.model import Tokens, Usuarios
from src.util.http_codes import Status


class AccessToken:

    def __init__(self):
        self.__secret_token = os.getenv('SECRET_TOKEN', 'shhhh!!')
        self.__exp_delta = int(os.getenv('TOKEN_EXP_DELTA', 60 * 60))
        self.__token_algorithm = os.getenv('TOKEN_ALGORITHM', 'HS256')

    def generate(self, payload):
        """ Función para generar un token

        Args:
            payload(dict): objeto con la información del token

        Returns:
            str: access token
        """
        payload['exp'] = (
            datetime.utcnow() + timedelta(seconds=self.__exp_delta)
        )

        return jwt.encode(
            payload, self.__secret_token,
            self.__token_algorithm)

    def validate(self, token):
        """ Función para validar un token

        Args:
            token(str): access token

        Returns:
            (bool, dict)
                bool: devuelve True en caso de que el token sea válido
                dict: información del token
        """
        if token:
            try:
                payload = jwt.decode(token, self.__secret_token,
                                     algorithms=[self.__token_algorithm])
                return True, payload
            except (jwt.DecodeError, jwt.ExpiredSignatureError):
                return False, None

        return False, None

    def update(self, token):
        """ Función para generar un nuevo token a partir del especificado

        Args:
            token(str): access token

        Returns:
            (bool, str)
                bool: devuelve True en caso de que el token sea válido
                str: access token
        """
        result, payload = self.validate(token)

        if(not result):
            return False, None

        return True, self.generate(payload)


def get_user_auth_from_token_header():
    """ Función para obtener el token de la cabecera (Authorization) y
        comprobar que es correcto

    Returns:
        src.model.model.Usuarios: información del usuario
    """
    access_token = AccessToken()
    token = request.headers.get('Authorization', None)
    result, payload = access_token.validate(token)

    if result:
        try:
            user_id = payload.get('user_id')
            token = Tokens.get(
                token=token,
                id_user=user_id
            )

            return DAOUser.get_user_by_id(user_id)
        except (Tokens.DoesNotExist, Usuarios.DoesNotExist):
            return None

    return None


def requires_auth(f):
    @wraps(f)
    def wrap(self, *args, **kwargs):
        user_auth = get_user_auth_from_token_header()

        if not user_auth:
            return DTOError(status_code=Status.HTTP_401_UNAUTHORIZED,
                            message="User not authenticated",
                            code="unhautorized").to_response()

        return f(self, user_auth, *args, **kwargs)
    return wrap


def check_auth(f):
    @wraps(f)
    def wrap(self, *args, **kwargs):
        user_auth = get_user_auth_from_token_header()
        return f(self, user_auth, *args, **kwargs)
    return wrap


def requires_admin_auth(f):
    @wraps(f)
    @requires_auth
    def wrap(self, user_auth, *args, **kwargs):
        if not user_auth.es_admin:
            return DTOError(status_code=Status.HTTP_401_UNAUTHORIZED,
                            message="Not admin user",
                            code="unhautorized").to_response()
        return f(self, *args, **kwargs)
    return wrap


def generate_salt():
    """ Función para generar un salt
    """
    return hashlib.md5(os.urandom(29)).hexdigest()


def encode_password(password, salt):
    """ Función para codificar una contraseña

    Args:
        password(str): contraseña
        salt(str): salt

    Returns:
        str: contraseña codificada
    """
    return hashlib.sha512((password + salt).encode()).hexdigest()


def check_passwords(password_db, password_user, salt):
    """ Función para comprobar que una contraseña dada se corresponde con la
        almacenada  codificada en la base de datos

    Args:
        password_db(str): contraseña almacenada (codificada)
        password_user(str): contraseña indicada (no codificada)
        salt(str): salt

    Returns:
        bool: devuelve si password_user se corresponde con la almacenada
    """
    return password_db == encode_password(password_user, salt)
