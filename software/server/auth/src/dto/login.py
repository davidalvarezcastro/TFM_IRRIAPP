from marshmallow import Schema, fields
from flask_restx import fields as fields_rest


class LoginSchema(Schema):

    email = fields.Email(
        required=True,
        data_key='email',
        error_messages={
            'invalid': 'Email must follow a correct email format!'
        })

    password = fields.String(
        required=True,
        data_key='password',
        error_messages={
            'invalid': 'Password must be a string!'
        })

    @staticmethod
    def doc(api, method=None):
        return api.model(LoginSchema.__name__, {
            'email': fields_rest.String,
            'password': fields_rest.String
        })
