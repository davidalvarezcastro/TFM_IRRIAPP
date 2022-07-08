import json
import http
from flask import Blueprint, Response, request

from api import jsend
from utils import logger_error
from api.settings import API_AREA_TYPES, API_GET_ALL_AREA_TYPES, MIMETYPE_JSON
from api.dto.area_type import ApiAreaTypesSchema
from domain.models.area_types import AreaType
from application.services.area_types import ServiceAreaTypes

blueprint = Blueprint('area_types', __name__)


@blueprint.route(API_AREA_TYPES, methods=['POST'])
def add():
    api_name = "Api Area Types (add)"
    status_code = http.HTTPStatus.CREATED

    try:
        try:
            new_type_data = ApiAreaTypesSchema().load(request.json)
        except Exception as e:
            logger_error(api_name, str(e))
            status_code = http.HTTPStatus.BAD_REQUEST
            raise Exception("Invalid request format data")

        try:
            new_type_id = ServiceAreaTypes().insert(
                type=AreaType(
                    id=new_type_data.get('type'),
                    description=new_type_data.get('description'),
                )
            )

            response = jsend.success({
                "type": new_type_id,
                "msg": f"Type {new_type_id} created"
            })
        except Exception as e:
            status_code = 500
            logger_error(api_name, str(e))
            raise e
    except Exception as e:
        logger_error(api_name, str(e))
        response = jsend.error(str(e))

    return Response(
        response=json.dumps(response),
        status=status_code,
        mimetype=MIMETYPE_JSON
    )


@blueprint.route(f'{API_AREA_TYPES}/<int:type>', methods=['PUT'])
def update(type: int):
    api_name = "Api Area Types (update)"
    status_code = http.HTTPStatus.OK

    try:
        try:
            updated_type_data = ApiAreaTypesSchema(only=ApiAreaTypesSchema.PUT_FIELDS).load(request.json)
        except Exception as e:
            logger_error(api_name, str(e))
            status_code = http.HTTPStatus.BAD_REQUEST
            raise Exception("Invalid request format data")

        try:
            type_db = ServiceAreaTypes().get_by_id(type=type)

            if type_db is None:
                status_code = http.HTTPStatus.NOT_FOUND
                response = jsend.error(f"Type {type} not found")
            else:
                type_db.description = updated_type_data.get('description')

                ServiceAreaTypes().update(
                    type=type_db
                )

                response = jsend.success({
                    "msg": f"Type {type} updated"
                })
        except Exception as e:
            logger_error(api_name, str(e))
            status_code = 500
            raise e
    except Exception as e:
        logger_error(api_name, str(e))
        response = jsend.error(str(e))

    return Response(
        response=json.dumps(response),
        status=status_code,
        mimetype=MIMETYPE_JSON
    )


@blueprint.route(f'{API_AREA_TYPES}/<int:type>', methods=['DELETE'])
def delete(type: int):
    api_name = "Api Area Types (delete)"
    status_code = http.HTTPStatus.OK

    try:
        try:
            type_db = ServiceAreaTypes().get_by_id(type=type)

            if type_db is None:
                status_code = http.HTTPStatus.NOT_FOUND
                response = jsend.error(f"Type {type} not found")

            else:
                ServiceAreaTypes().delete(
                    type=type_db
                )

                response = jsend.success({
                    "msg": f"Type {type} deleted"
                })
        except Exception as e:
            logger_error(api_name, str(e))
            status_code = 500
            raise e
    except Exception as e:
        logger_error(api_name, str(e))
        response = jsend.error(str(e))

    return Response(
        response=json.dumps(response),
        status=status_code,
        mimetype=MIMETYPE_JSON
    )


@blueprint.route(f'{API_AREA_TYPES}/<int:type>', methods=['GET'])
def get_by_id(type: int):
    api_name = "Api Area Types (get_by_id)"
    status_code = http.HTTPStatus.OK

    try:
        type_db = ServiceAreaTypes().get_by_id(type=type)

        if type_db is None:
            status_code = http.HTTPStatus.NOT_FOUND
            response = jsend.error(f"Type {type} not found")
        else:
            response = jsend.success(ApiAreaTypesSchema().dump(type_db))
    except Exception as e:
        logger_error(api_name, str(e))
        status_code = http.HTTPStatus.INTERNAL_SERVER_ERROR
        response = jsend.error(str(e))

    return Response(
        response=json.dumps(response),
        status=status_code,
        mimetype=MIMETYPE_JSON
    )


@blueprint.route(API_GET_ALL_AREA_TYPES, methods=['GET'])
def get_all():
    api_name = "Api Area Types (get_by_id)"
    status_code = http.HTTPStatus.OK

    try:
        response = jsend.success({
            "types": ApiAreaTypesSchema(many=True).dump(
                ServiceAreaTypes().get_all()
            )
        })
    except Exception as e:
        logger_error(api_name, str(e))
        status_code = http.HTTPStatus.INTERNAL_SERVER_ERROR
        response = jsend.error(str(e))

    return Response(
        response=json.dumps(response),
        status=status_code,
        mimetype=MIMETYPE_JSON
    )
