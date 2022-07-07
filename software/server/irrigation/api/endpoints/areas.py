import json
from flask import Blueprint, Response, request

from api.settings import MIMETYPE_JSON
from api import jsend
from api.dto.area_type import ApiAreaTypesSchema, QueryStringGet
from application.services.area_types import ServiceAreaTypes

blueprint = Blueprint('areas', __name__)


@blueprint.route('/area/type', methods=['POST'])
def add():
    return Response(
        response=json.dumps({'msg': 'pong'}),
        status=200,
        mimetype='application/json'
    )


@blueprint.route('/area/type', methods=['PUT'])
def update():
    return Response(
        response=json.dumps({'msg': 'pong'}),
        status=200,
        mimetype='application/json'
    )


@blueprint.route('/area/type/<int:type>', methods=['DELETE'])
def delete(type: int):
    return Response(
        response=json.dumps({'msg': 'pong'}),
        status=200,
        mimetype='application/json'
    )


@blueprint.route('/area/type/<int:type>', methods=['GET'])
def get_by_id(type: int):
    return Response(
        response=json.dumps({'msg': 'pong'}),
        status=200,
        mimetype='application/json'
    )


@blueprint.route('/area/types', methods=['GET'])
def get_all():
    try:
        args = QueryStringGet().load(request.args)
    except Exception:
        args = {}

    ServiceAreaTypes().get_all(all)

    try:
        # response = jsend.success({
        #     # serialize data
        #     "incidencias": IncidenciaApi(many=True).dump(incidencias)
        # })
        response = {

        }
    except Exception as es:
        status_code = 500
        response = jsend.error("Error formateando el listado de incidencias")

    return Response(
        response=json.dumps(response),
        status=status_code,
        mimetype=MIMETYPE_JSON
    )
