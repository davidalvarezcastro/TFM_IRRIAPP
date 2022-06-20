from flask_restplus import Namespace, Resource
from flask import request

from src.dto.dto import DTOError
from src.dto.user import DTOUsers, DTOUser
from src.dao.user import DAOUser
from src.util.http_codes import Status
from src.util.authentication import requires_admin_auth, check_auth
api_users = Namespace('users', description='User Api')


@api_users.route('')
class Users(Resource):

    @requires_admin_auth
    @check_auth
    @api_users.response(Status.HTTP_200_OK, 'Listado de usuarios',
                        [DTOUser.doc(api_users)])
    @api_users.response(Status.HTTP_404_NOT_FOUND, 'not_found',
                        DTOError.doc(api_users))
    def get(self, user_auth):
        users = DAOUser.get_users()
        es_publico = user_auth is None or not (
            user_auth is not None and user_auth.es_admin)

        return DTOUsers(
            Status.HTTP_200_OK,
            users,
            es_publico).to_response()
