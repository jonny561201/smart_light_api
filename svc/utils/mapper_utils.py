def map_light_groups(groups):
    return [__map_group(group) for group in groups]

def __map_group(group):
    return {
        'name': group.name,
        'id': group.id,
        'lights': [__map_light(light) for light in group.devices]
    }

def __map_light(light):
    return {
        'name': light.name,
        'id': light.id
    }