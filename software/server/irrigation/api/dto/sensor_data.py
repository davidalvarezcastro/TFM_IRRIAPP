""" DTO - sensor data historical schemas for rest api
"""
from marshmallow import Schema, pre_load, fields


class ApiHistoricalSensorDataSchema(Schema):
    controller_id = fields.Integer(
        allow_none=True,
        data_key='controller',
        error_messages={
            'invalid': '`controller` must be an Integer.'
        })
    area_id = fields.Integer(
        allow_none=True,
        data_key='area',
        error_messages={
            'invalid': '`area` must be a Integer.'
        })
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
    humidity = fields.Float(
        allow_none=True,
        data_key='humidity',
        error_messages={
            'invalid': '`humidity` must be a Float.'
        })
    temperature = fields.Float(
        allow_none=True,
        data_key='temperature',
        error_messages={
            'invalid': '`temperature` must be a Float.'
        })
    raining = fields.Boolean(
        allow_none=True,
        data_key='raining',
        error_messages={
            'invalid': '`raining` must be a Boolean.'
        })


class ApiSensorDataSchema(Schema):
    controller_id = fields.Integer(
        allow_none=True,
        data_key='controller',
        error_messages={
            'invalid': '`controller` must be an Integer.'
        })
    controller = fields.String(
        allow_none=True,
        data_key='controller_name',
        error_messages={
            'invalid': '`controller_name` must be a String.'
        })
    area_id = fields.Integer(
        allow_none=True,
        data_key='area',
        error_messages={
            'invalid': '`area` must be a Integer.'
        })
    area = fields.String(
        allow_none=True,
        data_key='area_name',
        error_messages={
            'invalid': '`area_name` must be a String.'
        })
    humidity = fields.Float(
        allow_none=True,
        data_key='humidity',
        error_messages={
            'invalid': '`humidity` must be a Float.'
        })
    temperature = fields.Float(
        allow_none=True,
        data_key='temperature',
        error_messages={
            'invalid': '`temperature` must be a Float.'
        })
    raining = fields.Boolean(
        allow_none=True,
        data_key='raining',
        error_messages={
            'invalid': '`raining` must be a Boolean.'
        })
    date = fields.String(
        allow_none=True,
        data_key='date',
        error_messages={
            'invalid': '`date` must be a String.'
        })
