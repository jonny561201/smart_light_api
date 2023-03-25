import tinytuya

GHOME_VERSION = 3.3


def set_switch_brightness(switch_id, brightness):
    #need to find switch ip/local key
    test = tinytuya.OutletDevice(switch_id, '192.168.1.220', local_key='', version=GHOME_VERSION)
    if brightness == 0:
        test.turn_off()
    else:
        test.turn_on()
        test.set_value(2, brightness * 10)


def set_switch_state(switch_id, on):
    #need to find switch ip/local key
    switch = tinytuya.OutletDevice(switch_id, '192.168.1.220', local_key='', version=GHOME_VERSION)
    switch.turn_on() if on else switch.turn_off()