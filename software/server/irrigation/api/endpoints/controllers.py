
import http
import json
from flask import Blueprint, Response, request

from api import jsend
from utils import logger_error
from api.settings import API_AREA_CONTROLLERS, API_GET_ALL_CONTROLLERS, MIMETYPE_JSON
from api.dto.controller import ApiControllersSchema, QueryStringGet
from domain.models.controllers import Controller
from application.services.controllers import ServiceControllers

blueprint = Blueprint('controllers', __name__)


@blueprint.route(API_AREA_CONTROLLERS, methods=['POST'])
def add():
    api_name = "Api Controllers (add)"
    status_code = http.HTTPStatus.CREATED

    try:
        try:
            new_type_data = ApiControllersSchema(only=ApiControllersSchema.POST_FIELDS).load(request.json)
        except Exception as e:
            logger_error(api_name, str(e))
            status_code = http.HTTPStatus.BAD_REQUEST
            raise Exception("Invalid request format data")

        try:
            new_controller_id = ServiceControllers().insert(
                controller=Controller(
                    area=new_type_data.get('area'),
                    name=new_type_data.get('name'),
                    description=new_type_data.get('description'),
                    visible=new_type_data.get('visible'),
                )
            )

            response = jsend.success({
                "controller": new_controller_id,
                "msg": f"Controller {new_type_data.get('name')} ({new_controller_id}) created"
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


@blueprint.route(f'{API_AREA_CONTROLLERS}/<int:controller>', methods=['PUT'])
def update(controller: int):
    api_name = "Api Controllers (update)"
    status_code = http.HTTPStatus.OK

    try:
        try:
            updated_type_data = ApiControllersSchema(only=ApiControllersSchema.PUT_FIELDS).load(request.json)
        except Exception as e:
            logger_error(api_name, str(e))
            status_code = http.HTTPStatus.BAD_REQUEST
            raise Exception("Invalid request format data")

        try:
            controller_db = ServiceControllers().get_by_id(controller=controller)

            if controller_db is None:
                status_code = http.HTTPStatus.NOT_FOUND
                response = jsend.error(f"Controller {controller} not found")
            else:

                for field in ApiControllersSchema.PUT_FIELDS:
                    if updated_type_data.get(field) is not None:
                        setattr(controller_db, field, updated_type_data.get(field))

                ServiceControllers().update(
                    controller=controller_db
                )

                response = jsend.success({
                    "msg": f"Controller {controller} updated"
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


@blueprint.route(f'{API_AREA_CONTROLLERS}/<int:controller>', methods=['DELETE'])
def delete(controller: int):
    api_name = "Api Controllers (delete)"
    status_code = http.HTTPStatus.OK

    try:
        try:
            controller_db = ServiceControllers().get_by_id(
                controller=controller,
                all_visibility=True  # we want to find all controllers
            )

            if controller_db is None:
                status_code = http.HTTPStatus.NOT_FOUND
                response = jsend.error(f"Controller {controller} not found")

            else:
                ServiceControllers().delete(
                    controller=controller_db
                )

                response = jsend.success({
                    "msg": f"Controller {controller} deleted"
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


@blueprint.route(f'{API_AREA_CONTROLLERS}/<int:controller>', methods=['GET'])
def get_by_id(controller: int):
    api_name = "Api Controllers (get_by_id)"
    status_code = http.HTTPStatus.OK

    try:
        # format query parameters
        try:
            args = QueryStringGet().load(request.args)
        except Exception:
            args = {}

        controller_db = ServiceControllers().get_by_id(
            controller=controller,
            all_visibility=args.get("all_visibility", False)
        )

        if controller_db is None:
            status_code = http.HTTPStatus.NOT_FOUND
            response = jsend.error(f"Controller {controller} not found")
        else:
            response = jsend.success(ApiControllersSchema().dump(controller_db))
    except Exception as e:
        logger_error(api_name, str(e))
        status_code = http.HTTPStatus.INTERNAL_SERVER_ERROR
        response = jsend.error(str(e))

    return Response(
        response=json.dumps(response),
        status=status_code,
        mimetype=MIMETYPE_JSON
    )


@blueprint.route(API_GET_ALL_CONTROLLERS, methods=['GET'])
def get_all():
    api_name = "Api Controllers (get_by_id)"
    status_code = http.HTTPStatus.OK

    try:
        # format query parameters
        try:
            args = QueryStringGet().load(request.args)
        except Exception:
            args = {}

        response = jsend.success({
            "controllers": ApiControllersSchema(many=True).dump(
                ServiceControllers().get_all(
                    all_visibility=args.get("all_visibility", False)
                )
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
