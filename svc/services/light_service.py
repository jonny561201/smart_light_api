from svc.repository.light_repository import LightDatabaseManager
from svc.utils import tuya_utils


def update_light_state(request):
    switch_id = request.get('lightId')
    brightness = request.get('brightness')
    on = request.get('on')

    tuya_utils.set_switch(switch_id, on, brightness)


def create_group(request):
    name = request['name']
    with LightDatabaseManager() as db:
        return db.create_new_group(name)


def delete_group(group_id):
    with LightDatabaseManager() as db:
        db.delete_group_by(group_id)


def get_light_groups():
    with LightDatabaseManager() as db:
        groups = db.get_light_groups()
        return list(map(__map_group, groups))


def set_light_group(request):
    on = request.get('on')
    brightness = request.get('brightness')
    group_id = request['groupId']

    with LightDatabaseManager() as db:
        lights = db.get_lights_by(group_id)
        for light in lights:
            tuya_utils.set_switch(light, on, brightness)


def get_unregistered_devices():
    devices = tuya_utils.scan_for_devices()
    with LightDatabaseManager() as db:
        registered_lights = db.get_all_lights()
        registered_id = [light.device_id for light in registered_lights]
        return [device for device in devices if device.get('id') not in registered_id ]


def __map_group(group):
    lights = list(map(__get_light_data, group.devices))
    has_lights = len(lights) > 0
    return {
        'groupName': group.name,
        'groupId': str(group.id),
        'lights': lights,
        'on': lights[0]['on'] if has_lights else False,
        'brightness': lights[0]['brightness'] if has_lights else 0
    }


def __get_light_data(light):
    return tuya_utils.get_light_status(light)
