""" DTO - area types schemas for rest api
"""
from marshmallow import Schema, pre_load, fields


class ApiAreaTypesSchema(Schema):
    type = fields.Integer(
        allow_none=True,
        data_key='id',
        error_messages={
            'invalid': '`id` must be an Integer.'
        })
    description = fields.String(
        allow_none=True,
        data_key='description',
        error_messages={
            'invalid': '`id` must be a String.'
        })

    PUT_FIELDS = [description.data_key]

    @pre_load
    def check_context(self, data, **kwargs):
        """ Checks context before deserializing the user data
        """
        # changing required to True if the load request is a POST request
        if 'put' in self.context:
            for field in self.PUT_FIELDS:
                self.fields[field].required = True

        return data
