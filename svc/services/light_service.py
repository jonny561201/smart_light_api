from svc.config.settings_state import Settings
from utils.file_utils import FileUtil
from utils.tuya_utils import set_switch_brightness


def update_light_state(data):
    switch_id = data.get('lightId')
    brightness = data.get('brightness')
    set_switch_brightness(switch_id, brightness)


def get_light_groups():
    file_util = FileUtil.get_instance()
    return file_util.get_all_light_groups()


def set_light_group(request):
    settings = Settings.get_instance()
    file_util = FileUtil().get_instance()
    file_util.get_json_file(settings.light_file)
