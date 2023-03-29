def map_light_groups(groups):
    return [__map_group(group) for group in groups]

def __map_group(group):
    return {
        'groupName': group.name,
        'groupId': group.id,
        'lights': [__map_light(light) for light in group.devices]
    }

def __map_light(light):
    return {
        'lightName': light.name,
        'lightId': light.id
    }

# [
#     { groupId: 1, groupName: 'Living Room', brightness: 100, on: true, lights: [
#         { brightness: 80, lightName: 'lamp', lightId: 2, groupId: 1, on: true },
#         { brightness: 10, lightName: 'desk', lightId: 3, groupId: 1, on: true },
#     ]
#       }
# ],