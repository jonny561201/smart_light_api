import json

from flask import request, Response, Blueprint

from svc.services import light_service

LIGHT_BLUEPRINT = Blueprint('light_blueprint', __name__, url_prefix='/api/lights')
DEFAULT_HEADERS = {'Content-Type': 'text/json'}


@LIGHT_BLUEPRINT.route('/health', methods=['GET'])
def get_health():
    return 'success'


@LIGHT_BLUEPRINT.route('/light/state', methods=['POST'])
def set_light_state():
    api_key = request.headers.get('LightApiKey')
    data = json.loads(request.data.decode('UTF-8'))

    light_service.update_light_state(api_key, data)
    return Response(status=200, headers=DEFAULT_HEADERS)


@LIGHT_BLUEPRINT.route('/groups', methods=['GET'])
def get_all_light_groups():
    api_key = request.headers.get('LightApiKey')
    content = light_service.get_light_groups(api_key)
    return Response(json.dumps(content), status=200, headers=DEFAULT_HEADERS)


@LIGHT_BLUEPRINT.route('/group/state', methods=['POST'])
def set_light_group():
    api_key = request.headers.get('LightApiKey')
    data = json.loads(request.data.decode('UTF-8'))

    light_service.set_light_group(api_key, data)
    return Response(status=200, headers=DEFAULT_HEADERS)


@LIGHT_BLUEPRINT.route('/group/create', methods=['POST'])
def create_new_group():
    api_key = request.headers.get('LightApiKey')
    data = json.loads(request.data.decode('UTF-8'))

    group_id = light_service.create_group(api_key, data)
    return Response(json.dumps(group_id), status=200, headers=DEFAULT_HEADERS)


@LIGHT_BLUEPRINT.route('/group/<group_id>', methods=['DELETE'])
def delete_group_by_id(group_id):
    api_key = request.headers.get('LightApiKey')
    light_service.delete_group(api_key, group_id)
    return Response(status=200, headers=DEFAULT_HEADERS)


@LIGHT_BLUEPRINT.route('/scan', methods=['GET'])
def scan_unregistered_devices():
    api_key = request.headers.get('LightApiKey')
    content = light_service.scan_unregistered_devices(api_key)
    return Response(json.dumps(content), status=200, headers=DEFAULT_HEADERS)


@LIGHT_BLUEPRINT.route('/unregistered', methods=['GET'])
def get_unregistered_devices():
    api_key = request.headers.get('LightApiKey')
    content = light_service.get_unregistered_devices(api_key)
    return Response(json.dumps(content), status=200, headers=DEFAULT_HEADERS)


@LIGHT_BLUEPRINT.route('/group/assign', methods=['POST'])
def assign_light_group():
    api_key = request.headers.get('LightApiKey')
    data = json.loads(request.data.decode('UTF-8'))

    light_service.assign_group(api_key, data)
    return Response(status=200, headers=DEFAULT_HEADERS)


@LIGHT_BLUEPRINT.route('/group/update', methods=['POST'])
def update_light_group():
    api_key = request.headers.get('LightApiKey')
    data = json.loads(request.data.decode('UTF-8'))

    light_service.update_group(api_key, data)
    return Response(status=200, headers=DEFAULT_HEADERS)

# TODO: distinguish between switch/dimmer
# TODO: get_all_light_groups needs to return unassigned lights too
# TODO: how to kick off job and start task (celery uses a broker like redis/rabbitmq?)
