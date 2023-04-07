import tinytuya

from svc.config.tuya_constants import GHOME
from svc.utils.mapper_utils import map_light


def set_switch(light, on, brightness):
    switch = tinytuya.OutletDevice(light.device_id, light.ip_address, local_key=light.local_key, version=GHOME.VERSION)
    if on and brightness:
        switch.turn_on()
        switch.set_value(2, brightness * 10)
    elif on:
        switch.turn_on()
    else:
        switch.turn_off()


def set_switch_brightness(light, brightness):
    switch = tinytuya.OutletDevice(light.device_id, light.ip_address, local_key=light.local_key, version=GHOME.VERSION)
    if brightness == 0:
        switch.turn_off()
    else:
        switch.turn_on()
        switch.set_value(2, brightness * 10)


def set_switch_state(light, on):
    switch = tinytuya.OutletDevice(light.device_id, light.ip_address, local_key=light.local_key, version=GHOME.VERSION)
    switch.turn_on() if on else switch.turn_off()


def get_light_status(light):
    if light.device_type.name == 'outlet':
        switch = tinytuya.OutletDevice(light.device_id, light.ip_address, local_key=light.local_key, version=GHOME.VERSION)
        status = switch.status().get('dps')
        return map_light(light, status)


# def get_moar_light_status(light):
#     switch = tinytuya.OutletDevice(light['deviceId'], light['ipAddress'], local_key=light['localKey'], version=GHOME.VERSION)
#     status = switch.status().get('dps')
#     return map_moar_light(light, status)


def scan_for_devices():
    devices = tinytuya.deviceScan()
    return [v for k, v in devices.items()]
