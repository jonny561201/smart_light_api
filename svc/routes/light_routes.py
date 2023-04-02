import json

from flask import request, Response, Blueprint

from svc.services import light_service

LIGHT_BLUEPRINT = Blueprint('light_blueprint', __name__, url_prefix='/lights')
DEFAULT_HEADERS = {'Content-Type': 'text/json'}


@LIGHT_BLUEPRINT.route('/light/state', methods=['POST'])
def set_light_state():
    data = json.loads(request.data.decode('UTF-8'))
    light_service.update_light_state(data)
    return Response(status=200, headers=DEFAULT_HEADERS)


@LIGHT_BLUEPRINT.route('/groups', methods=['GET'])
def get_all_light_groups():
    content = light_service.get_light_groups()
    return Response(json.dumps(content), status=200, headers=DEFAULT_HEADERS)


@LIGHT_BLUEPRINT.route('/group/state', methods=['POST'])
def set_light_group():
    data = json.loads(request.data.decode('UTF-8'))
    light_service.set_light_group(data)
    return Response(status=200, headers=DEFAULT_HEADERS)