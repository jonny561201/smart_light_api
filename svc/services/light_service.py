import tinytuya


def update_light_state(data):
    light_id = data.get('lightId')
    brightness = data.get('brightness')
    test = tinytuya.OutletDevice(light_id, '192.168.1.220', local_key='', version=3.3)
    if brightness == 0:
        test.turn_off()
    else:
        test.turn_on()
        test.set_value(2, brightness * 10)
