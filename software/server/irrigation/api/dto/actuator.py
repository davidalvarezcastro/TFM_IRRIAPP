""" DTO - actuator confirmation historical schemas for rest api
"""
from marshmallow import Schema, pre_load, fields


class ApiHistoricalActuatorActivationSchema(Schema):
    start_date = fields.String(
        allow_none=True,
        data_key='start_date',
        error_messages={
            'invalid': '`start_date` must be a String.'
        })
    end_date = fields.String(
        allow_none=True,
        data_key='end_date',
        error_messages={
            'invalid': '`start_date` must be a String.'
        })


class ApiActuatorActivationSchema(Schema):
    area_id = fields.Integer(
        allow_none=True,
        data_key='area',
        error_messages={
            'invalid': '`area` must be a Integer.'
        })
    # # TODO: normalize irrigation < -> activated MongoDB
    # irrigation = fields.Boolean(
    #     allow_none=True,
    #     data_key='irrigation',
    #     error_messages={
    #         'invalid': '`irrigation` must be a Boolean.'
    #     })
    start_date = fields.String(
        allow_none=True,
        data_key='start_date',
        error_messages={
            'invalid': '`start_date` must be a String.'
        })
    end_date = fields.String(
        allow_none=True,
        data_key='end_date',
        error_messages={
            'invalid': '`start_date` must be a String.'
        })
