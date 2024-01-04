from werkzeug.exceptions import Unauthorized

from svc.config.settings_state import Settings


def is_valid(api_key):
    settings = Settings.get_instance()
    valid_api_key = settings.api_key

    if api_key != valid_api_key:
        raise Unauthorized
