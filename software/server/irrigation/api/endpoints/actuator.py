
import datetime
import http
import json
from flask import Blueprint, Response, request

from api import jsend
from utils import logger_error, get_datetime_from_string
from api.settings import MIMETYPE_JSON, API_GET_HISTORICAL_ACTUATOR_DATA_AREA
from api.dto.actuator import ApiHistoricalActuatorActivationSchema, ApiActuatorActivationSchema
from application.services.irrigation_data import ServiceIrrigationHistoric
from domain.models.irrigation_data import QueryIrrigationData


blueprint = Blueprint('actuator', __name__)

# TODO: normalize irrigation <-> actuator cnfirmation


@blueprint.route(API_GET_HISTORICAL_ACTUATOR_DATA_AREA.format(area="<int:area>"),
                 methods=['GET'])
def get_filter(area: int):
    api_name = "Api Historical Data actuator activation (get_filter)"
    status_code = http.HTTPStatus.OK

    try:
        # format query parameters
        try:
            args = ApiHistoricalActuatorActivationSchema().load(request.args)
        except Exception as e:
            args = {}

        # processing dates
        start_date = get_datetime_from_string(args.get(
            'start_date')) if args.get(
            'start_date', None) is not None else None
        end_date = get_datetime_from_string(args.get(
            'end_date')) if args.get(
            'end_date', None) is not None else None

        result = ServiceIrrigationHistoric().get(
            query=QueryIrrigationData(
                area_id=area,
                start_date=start_date,
                end_date=end_date,
            )
        )

        response = jsend.success({
            "actuator_activation": ApiActuatorActivationSchema(many=True).dump(result)
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
