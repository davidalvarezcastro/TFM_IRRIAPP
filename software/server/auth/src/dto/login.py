from marshmallow import Schema, fields
from flask_restx import fields as fields_rest


class LoginSchema(Schema):

    user = fields.String(
        required=True,
        data_key='user',
        error_messages={
            'invalid': 'User must be a string!'
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
            'user': fields_rest.String,
            'password': fields_rest.String
        })
