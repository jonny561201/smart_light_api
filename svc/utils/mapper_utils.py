from svc.config.tuya_constants import DeviceStates


def map_light(light, status):
    currently_on = status.get(DeviceStates.ON)
    return {
        'lightName': light.name,
        'lightId': str(light.id),
        'groupId': str(light.group_id),
        'on': currently_on,
        'brightness': status.get(DeviceStates.BRIGHTNESS) if currently_on else 0
    }


def map_unregistered_light(light):
    return {
        'name': light.name,
        'ipAddress': light.ip_address
    }

# def map_moar_light(light, status):
#     return {
#         'lightName': light['name'],
#         'lightId': light['id'],
#         'groupId': light['groupId'],
#         'on': status.get(DeviceStates.ON),
#         'brightness': status.get(DeviceStates.BRIGHTNESS)
#     }

# [
#     { groupId: 1, groupName: 'Living Room', brightness: 100, on: true, lights: [
#         { brightness: 80, lightName: 'lamp', lightId: 2, groupId: 1, on: true },
#         { brightness: 10, lightName: 'desk', lightId: 3, groupId: 1, on: true },
#     ]
#       }
# ],