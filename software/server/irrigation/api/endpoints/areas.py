
import http
import json
from flask import Blueprint, Response, request

from api import jsend
from utils import logger_error
from api.settings import API_AREA_AREAS, API_GET_ALL_AREAS, MIMETYPE_JSON
from api.dto.area import ApiAreasSchema, QueryStringGet
from domain.models.areas import Area
from application.services.areas import ServiceAreas

blueprint = Blueprint('areas', __name__)


@blueprint.route(API_AREA_AREAS, methods=['POST'])
def add():
    api_name = "Api Areas (add)"
    status_code = http.HTTPStatus.CREATED

    try:
        try:
            new_type_data = ApiAreasSchema(only=ApiAreasSchema.POST_FIELDS).load(request.json)
        except Exception as e:
            logger_error(api_name, str(e))
            status_code = http.HTTPStatus.BAD_REQUEST
            raise Exception("Invalid request format data")

        try:
            new_area_id = ServiceAreas().insert(
                area=Area(
                    name=new_type_data.get('name'),
                    description=new_type_data.get('description'),
                    visible=new_type_data.get('visible'),
                )
            )

            response = jsend.success({
                "area": new_area_id,
                "msg": f"Area {new_type_data.get('name')} ({new_area_id}) created"
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


@blueprint.route(f'{API_AREA_AREAS}/<int:area>', methods=['PUT'])
def update(area: int):
    api_name = "Api Areas (update)"
    status_code = http.HTTPStatus.OK

    try:
        try:
            updated_type_data = ApiAreasSchema(only=ApiAreasSchema.PUT_FIELDS).load(request.json)
        except Exception as e:
            logger_error(api_name, str(e))
            status_code = http.HTTPStatus.BAD_REQUEST
            raise Exception("Invalid request format data")

        try:
            area_db = ServiceAreas().get_by_id(area=area)

            if area_db is None:
                status_code = http.HTTPStatus.NOT_FOUND
                response = jsend.error(f"Area {area} not found")
            else:
                if updated_type_data.get('description') is not None:
                    area_db.description = updated_type_data.get('description')
                if updated_type_data.get('visible') is not None:
                    area_db.visible = updated_type_data.get('visible')

                ServiceAreas().update(
                    area=area_db
                )

                response = jsend.success({
                    "msg": f"Area {area} updated"
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


@blueprint.route(f'{API_AREA_AREAS}/<int:area>', methods=['DELETE'])
def delete(area: int):
    api_name = "Api Areas (delete)"
    status_code = http.HTTPStatus.OK

    try:
        try:
            area_db = ServiceAreas().get_by_id(
                area=area,
                all_visibility=True  # we want to find all areas
            )

            if area_db is None:
                status_code = http.HTTPStatus.NOT_FOUND
                response = jsend.error(f"Area {area} not found")

            else:
                ServiceAreas().delete(
                    area=area_db
                )

                response = jsend.success({
                    "msg": f"Area {area} deleted"
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


@blueprint.route(f'{API_AREA_AREAS}/<int:area>', methods=['GET'])
def get_by_id(area: int):
    api_name = "Api Areas (get_by_id)"
    status_code = http.HTTPStatus.OK

    try:
        # format query parameters
        try:
            args = QueryStringGet().load(request.args)
        except Exception:
            args = {}

        area_db = ServiceAreas().get_by_id(
            area=area,
            all_visibility=args.get("all_visibility", False)
        )

        if area_db is None:
            status_code = http.HTTPStatus.NOT_FOUND
            response = jsend.error(f"Area {area} not found")
        else:
            response = jsend.success(ApiAreasSchema().dump(area_db))
    except Exception as e:
        logger_error(api_name, str(e))
        status_code = http.HTTPStatus.INTERNAL_SERVER_ERROR
        response = jsend.error(str(e))

    return Response(
        response=json.dumps(response),
        status=status_code,
        mimetype=MIMETYPE_JSON
    )


@blueprint.route(API_GET_ALL_AREAS, methods=['GET'])
def get_all():
    api_name = "Api Areas (get_by_id)"
    status_code = http.HTTPStatus.OK

    try:
        # format query parameters
        try:
            args = QueryStringGet().load(request.args)
        except Exception:
            args = {}

        response = jsend.success({
            "areas": ApiAreasSchema(many=True).dump(
                ServiceAreas().get_all(
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
