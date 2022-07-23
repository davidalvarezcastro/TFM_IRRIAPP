import marshmallow as ma
from .dto import DTOBase
from flask_restx import fields as fields_rest


class UserSchema(ma.Schema):

    class Meta:
        unknown = ma.EXCLUDE

    username = ma.fields.String(
        data_key='username',
        error_messages={
            'invalid': 'Tiene que ser String'
        }
    )
    password = ma.fields.String(
        data_key='password',
        error_messages={
            'invalid': 'Tiene que ser String'
        }
    )
    email = ma.fields.Email(
        data_key='email',
        error_messages={
            'invalid': 'Tiene que ser de tipo Email (usuario@televes.com)'
        }
    )
    es_admin = ma.fields.Boolean(
        data_key='es_admin',
        error_messages={
            'invalid': 'Tiene que ser Bool'
        }
    )

    PUT_FIELDS = [
        password.data_key,
        es_admin.data_key,
    ]
    POST_FIELDS = [
        username.data_key,
        password.data_key,
        email.data_key,
    ]

    @ma.pre_load
    def check_context(self, data, **kwargs):
        """ Comprueba el contexto de la aplicación antes de deserializar
            los datos del usuerio
        """
        if 'post' in self.context:
            for field in self.POST_FIELDS:
                self.fields[field].required = True

        return data


class DTOUser(DTOBase):

    def __init__(self, status_code, user, is_public=True):
        self.user = user
        self.is_public = is_public

        super().__init__(status_code=status_code, message=None)

    def to_json(self):
        user_json = {
            'email': self.user.email,
            'username': self.user.username,
        }

        if not self.is_public:
            user_json['esAdmin'] = bool(self.user.es_admin)
            user_json['activo'] = bool(self.user.activo)

        return user_json

    def to_response(self):
        return self.to_json(), self.status_code

    @staticmethod
    def doc(api, method=None):
        if method is None:
            return api.model(DTOUser.__name__, {
                'email': fields_rest.String,
                'username': fields_rest.String,
            })
        elif method == 'POST':
            return api.model(DTOUser.__name__ + '_' + method, {
                'username': fields_rest.String,
                'email': fields_rest.String,
                'password': fields_rest.String,
            })
        elif method == 'PUT':
            return api.model(DTOUser.__name__ + '_' + method, {
                'password': fields_rest.String,
                'es_admin': fields_rest.Boolean,
            })


class DTOUsers(DTOBase):

    def __init__(self, status_code, users, is_public=True):
        self.users = users
        self.is_public = is_public

        super().__init__(status_code=status_code, message=None)

    def to_response(self):
        return [DTOUser(
            self.status_code,
            user,
            self.is_public
        ).to_json() for user in self.users], self.status_code
