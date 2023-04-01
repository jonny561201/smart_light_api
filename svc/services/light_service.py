from svc.repository.light_repository import LightDatabaseManager
from svc.utils import tuya_utils


def update_light_state(data):
    switch_id = data.get('lightId')
    brightness = data.get('brightness')
    tuya_utils.set_switch_brightness(switch_id, brightness)


def get_light_groups():
    with LightDatabaseManager() as db:
        groups = db.get_light_groups()
        return list(map(__create_group, groups))


def set_light_group(request):
    on = request.get('on')
    brightness = request.get('brightness')
    group_id = request['groupId']

    with LightDatabaseManager() as db:
        lights = db.get_lights_by(group_id)
        for light in lights:
            tuya_utils.set_switch(light, on, brightness)


def __create_group(group):
    lights = list(map(__get_light_data, group.devices))
    return {
        'groupName': group.name,
        'groupId': str(group.id),
        'lights': lights,
        # 'on': lights[0]
    }


def __get_light_data(light):
    return tuya_utils.get_light_status(light)
