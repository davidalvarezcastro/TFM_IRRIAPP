# -*- coding: utf-8 -*-
"""Jsend Specification

{
    status: 'success',
    data: {},
}

{
    status: 'fail',
    data: {},
}

{
    status: 'error',
    message: '',
    code: ,           (optional)
    data: {},         (optional)
}

https://labs.omniti.com/labs/jsend
"""


def success(data=None):
    """success response

    Args:
        data (dict, optional):

    Returns:
        dict:
    """
    if data is None:
        data = {}
    if not isinstance(data, dict):
        raise ValueError('data must be dict')
    jsend_response = {
        'status': 'success',
        'data': data,
    }
    return jsend_response


def fail(data=None):
    """fail response

    Args:
        data (dict, optional):

    Returns:
        dict:
    """
    if data is None:
        data = {}
    if not isinstance(data, dict):
        raise ValueError('data must be dict')
    jsend_response = {
        'status': 'fail',
        'data': data,
    }
    return jsend_response


def error(message, code=None, data=None):
    """error response

    Args:
        message (str)
        code (str, optional): numerical error code
        data (dict, optional): data

    Returns:
        dict:
    """
    if not isinstance(message, str):
        raise ValueError('message must be string')
    jsend_response = {
        'status': 'error',
        'message': message,
    }
    if code:
        if not isinstance(code, int):
            raise ValueError('code must be int')
        jsend_response.update({'code': code, })
    if data:
        if not isinstance(data, dict):
            raise ValueError('data must be dict')
        jsend_response.update({'data': data, })
    return jsend_response
