""" DTO - area types schemas for rest api
"""
from marshmallow import Schema, pre_load, fields


class QueryStringGet(Schema):
    all_visibility = fields.Boolean(
        data_key='all_visibility',
        error_messages={
            'invalid': '`all_visibility` must be a Boolean.'
        })


class ApiAreasSchema(Schema):
    id = fields.Integer(
        allow_none=True,
        data_key='id',
        error_messages={
            'invalid': '`id` must be an Integer.'
        })
    name = fields.String(
        data_key='name',
        error_messages={
            'invalid': '`name` must be a String.'
        })
    description = fields.String(
        allow_none=True,
        data_key='description',
        error_messages={
            'invalid': '`description` must be a String.'
        })
    visible = fields.Boolean(
        allow_none=True,
        data_key='visible',
        error_messages={
            'invalid': '`visible` must be an Boolean.'
        })
    date = fields.String(
        allow_none=True,
        data_key='date',
        error_messages={
            'invalid': '`date` must be a String.'
        })

    POST_FIELDS = [name.data_key, description.data_key, visible.data_key]
    PUT_FIELDS = [description.data_key, visible.data_key]

    @pre_load
    def check_context(self, data, **kwargs):
        """ Checks context before deserializing the area data
        """
        if 'post' in self.context:
            for field in self.PUT_FIELDS:
                self.fields[field].required = True

        return data
