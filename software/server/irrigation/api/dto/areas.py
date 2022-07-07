""" DTO - area types schemas for rest api
"""
import marshmallow as ma


class QueryStringGet(ma.Schema):
    all_visibility = ma.fields.Boolean(
        data_key='all_visibility',
        error_messages={
            'invalid': '`all_visibility` must be an Boolean.'
        })


class ApiAreaTypesSchema(ma.Schema):
    type = ma.fields.Integer(
        data_key='id',
        error_messages={
            'invalid': '`id` must be an Integer.'
        })
    description = ma.fields.String(
        allow_none=True,
        data_key='description',
        error_messages={
            'invalid': '`id` must be a String.'
        })
