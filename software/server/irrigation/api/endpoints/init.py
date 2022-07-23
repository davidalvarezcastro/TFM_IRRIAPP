import json
from flask import Blueprint, Response

blueprint = Blueprint('init', __name__)


@blueprint.route('/ping', methods=['GET'])
def ping():
    return Response(
        response=json.dumps({'msg': 'pong'}),
        status=200,
        mimetype='application/json'
    )
