import json

from flask import request, Response, Blueprint

from svc.services.light_service import update_light_state

LIGHT_BLUEPRINT = Blueprint('light_blueprint', __name__, url_prefix='/lights')
DEFAULT_HEADERS = {'Content-Type': 'text/json'}


@LIGHT_BLUEPRINT.route('/light/state', methods=['POST'])
def set_light_state():
    data = json.loads(request.data.decode('UTF-8'))
    update_light_state(data)
    return Response(status=200, headers=DEFAULT_HEADERS)
