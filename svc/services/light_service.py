from svc.config.settings_state import Settings
from svc.repository.light_repository import LightDatabaseManager
from svc.utils.file_utils import FileUtil
from svc.utils.tuya_utils import set_switch_brightness, get_light_status


def update_light_state(data):
    switch_id = data.get('lightId')
    brightness = data.get('brightness')
    set_switch_brightness(switch_id, brightness)


def get_light_groups():
    with LightDatabaseManager() as db:
        groups = db.get_light_groups()
        return list(map(__create_group, groups))


def set_light_group(request):
    with LightDatabaseManager() as db:
        db.get_light_groups()


def __create_group(group):
    return {
        'groupName': group.name,
        'groupId': str(group.id),
        'lights': list(map(__get_light_data, group.devices))
    }


def __get_light_data(light):
    return get_light_status(light)
