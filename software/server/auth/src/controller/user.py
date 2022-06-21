from flask_restx import Namespace, Resource
from flask import request
import marshmallow as ma

from src.model.model import Usuarios
from src.dto.user import UserSchema
from src.dto.dto import DTOError, DTOBase
from src.dto.user import DTOUser
from src.util.http_codes import Status
from src.util.database import requires_user
from src.util.authentication import requires_auth, requires_admin_auth, \
    check_auth, encode_password, generate_salt

api_user = Namespace('user', description='user service')


@api_user.route('/<string:user_id>')
@api_user.doc(params={'user_id': {'description': 'Username', 'type': 'string'}})
class User(Resource):

    @requires_user
    @check_auth
    @api_user.response(Status.HTTP_200_OK, 'Información del usuario',
                       DTOUser.doc(api_user))
    @api_user.response(Status.HTTP_404_NOT_FOUND, 'not_found',
                       DTOError.doc(api_user))
    def get(self, user_auth, user):
        es_publico = user_auth is None or not (
            user_auth is not None and user_auth.es_admin)
        return DTOUser(
            Status.HTTP_200_OK,
            user,
            es_publico
        ).to_response()

    @requires_user
    @requires_admin_auth
    @api_user.response(200, 'Usuario eliminado')
    def delete(self, user):
        # if user_auth.username == user.username or user_auth.es_admin:
        #     DAOUser.delete_user_by_username(user.username)
        #     return DTOBase(Status.HTTP_200_OK, {
        #         "msg": "Usuario eliminado!"
        #     }).to_response()
        # else:
        #     return DTOError(status_code=Status.HTTP_401_UNAUTHORIZED,
        #                     message="User not authenticated",
        #                     code="unhautorized").to_response()
        try:
            user.activo = False
            user.save()
        except Exception:
            pass

        return DTOBase(Status.HTTP_200_OK, {
            "msg": "Usuario eliminado!"
        }).to_response()

    @requires_user
    @requires_auth
    @api_user.doc(body=DTOUser.doc(api_user, method='PUT'))
    @api_user.response(Status.HTTP_200_OK, 'Información actualizada',
                       DTOUser.doc(api_user))
    @api_user.response(Status.HTTP_404_NOT_FOUND, 'not_found',
                       DTOError.doc(api_user))
    def put(self, user_auth, user):
        @requires_admin_auth
        def update_permisos(user):
            user.es_admin = u['es_admin'] if 'es_admin' in u else user.es_admin

        if user_auth.username == user.username or user_auth.es_admin:
            u = UserSchema(only=UserSchema.PUT_FIELDS).load(request.json)
            update_permisos(user)
            user.password = encode_password(
                u['password'], user.salt)if 'password' in u else user.password
            user.save()
        else:
            return DTOError(status_code=Status.HTTP_401_UNAUTHORIZED,
                            message="User not authenticated",
                            code="unhautorized").to_response()

        return DTOUser(
            Status.HTTP_200_OK, user, not user_auth.es_admin
        ).to_response()


@api_user.route('')
class NewUser(Resource):

    @requires_admin_auth
    @api_user.expect(DTOUser.doc(api_user, method='POST'))
    @api_user.response(Status.HTTP_201_CREATED, 'Información del nuevo usuario',
                       DTOUser.doc(api_user))
    @api_user.response(Status.HTTP_400_BAD_REQUEST, 'bad_request',
                       DTOError.doc(api_user))
    @api_user.response(Status.HTTP_500_INTERNAL_SERVER_ERROR, 'database_error',
                       DTOError.doc(api_user))
    def post(self):
        try:
            u = UserSchema(context={'post': True}).load(request.json)
        except ma.ValidationError:
            return DTOError(status_code=Status.HTTP_400_BAD_REQUEST,
                            message='Required fields are not satisfied',
                            code="bad_request").to_response()

        try:
            salt = generate_salt()
            user = Usuarios(
                username=u['username'],
                email=u['email'],
                password=encode_password(u['password'], salt),
                salt=salt
            )
            if 'es_admin' in u:
                user.es_admin = u['es_admin']

            user.save(force_insert=True)
        except Exception:
            return DTOError(status_code=Status.HTTP_500_INTERNAL_SERVER_ERROR,
                            message="Error creating user",
                            code="database_error").to_response()

        return DTOUser(Status.HTTP_201_CREATED, user, False).to_response()
