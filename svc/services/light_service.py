import tinytuya

from svc.config.settings_state import Settings
from svc.utils import file_utils


def update_light_state(data):
    light_id = data.get('lightId')
    brightness = data.get('brightness')
    test = tinytuya.OutletDevice(light_id, '192.168.1.220', local_key='', version=3.3)
    if brightness == 0:
        test.turn_off()
    else:
        test.turn_on()
        test.set_value(2, brightness * 10)


def get_light_groups():
    settings = Settings.get_instance()
    content = file_utils.get_json_file(settings.light_file)
    if not content:
        return file_utils.create_json_file(settings.light_file)
    return content


def set_light_group(request):
    settings = Settings.get_instance()
    file_utils.get_json_file(settings.light_file)
