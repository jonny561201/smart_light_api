from flask import Response, Blueprint

LIGHT_BLUEPRINT = Blueprint('light_blueprint', __name__, url_prefix='/lights')
DEFAULT_HEADERS = {'Content-Type': 'text/json'}


@LIGHT_BLUEPRINT.route('/light/state', methods=['POST'])
def set_light_state():
    return Response(status=200, headers=DEFAULT_HEADERS)
