
import datetime
import http
import json
from flask import Blueprint, Response, request

from api import jsend
from utils import logger_error, get_datetime_from_string
from api.settings import MIMETYPE_JSON, API_GET_HISTORIC_SENSOR_DATA_CONTROLLER
from api.dto.sensor_data import ApiHistoricalSensorDataSchema, ApiSensorDataSchema
from application.services.sensor_data import ServiceSensorsHistoric
from domain.models.sensor_data_historic import QuerySensorData


blueprint = Blueprint('historical_sensor_data', __name__)


@blueprint.route(API_GET_HISTORIC_SENSOR_DATA_CONTROLLER.format(controller="<int:controller>"),
                 methods=['GET'])
def get_filter(controller: int):
    api_name = "Api Historical Data Sensors (get_filter)"
    status_code = http.HTTPStatus.OK

    try:
        # format query parameters
        try:
            args = ApiHistoricalSensorDataSchema().load(request.args)
        except Exception as e:
            args = {}

        # processing dates
        start_date = get_datetime_from_string(args.get(
            'start_date')) if args.get(
            'start_date', None) is not None else None
        end_date = get_datetime_from_string(args.get(
            'end_date')) if args.get(
            'end_date', None) is not None else None

        result = ServiceSensorsHistoric().get(
            query=QuerySensorData(
                controller_id=controller,
                area_id=args.get('area_id', None),
                humidity=args.get('humidity', None),
                temperature=args.get('temperature', None),
                raining=args.get('raining', None),
                start_date=start_date,
                end_date=end_date,
            )
        )

        response = jsend.success({
            "sensor_data": ApiSensorDataSchema(many=True).dump(result)
        })
    except Exception as e:
        status_code = http.HTTPStatus.INTERNAL_SERVER_ERROR
        response = jsend.error(str(e))

    return Response(
        response=json.dumps(response),
        status=status_code,
        mimetype=MIMETYPE_JSON
    )
