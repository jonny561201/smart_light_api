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


@LIGHT_BLUEPRINT.route('/group/create', methods=['POST'])
def create_new_group():
    data = json.loads(request.data.decode('UTF-8'))
    group_id = light_service.create_group(data)
    return Response(json.dumps(group_id), status=200, headers=DEFAULT_HEADERS)


@LIGHT_BLUEPRINT.route('/group/<group_id>', methods=['DELETE'])
def delete_group_by_id(group_id):
    light_service.delete_group(group_id)
    return Response(status=200, headers=DEFAULT_HEADERS)


@LIGHT_BLUEPRINT.route('/unregistered', methods=['GET'])
def get_unregistered_lights():
    content = light_service.get_unregistered_devices()
    return Response(json.dumps(content), status=200, headers=DEFAULT_HEADERS)

# TODO: endpoint to add items to the group/remove item from group
# TODO: endpoint to scan for new lights return job guid and endpoint to check status of job
# TODO: how to kick off job and start task (celery uses a broker like redis/rabbitmq?)
