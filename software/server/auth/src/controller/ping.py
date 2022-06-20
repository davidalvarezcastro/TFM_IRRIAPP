
from flask_restplus import Namespace, Resource, fields as fields_rest

from src.util.http_codes import Status
from src.dto.dto import DTOError, DTOBase


api_ping = Namespace('ping', description='PingPong Api')


@api_ping.route('/')
class Ping(Resource):
    @api_ping.response(Status.HTTP_200_OK, 'pong', 
        api_ping.model('DTOPing', {
                    'msg': fields_rest.String("pong"),
                })
    )
    def get(self):
        return DTOBase(Status.HTTP_200_OK, {
                    "msg": "pong"
                }).to_response()
