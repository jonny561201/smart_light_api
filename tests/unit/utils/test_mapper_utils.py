import uuid

from svc.config.tuya_constants import DeviceStates
from svc.repository.models.lights import DeviceGroups, Devices, UnregisteredDevices
from svc.utils.mapper_utils import map_light, map_unregistered_light


class TestMapperUtils:
    GROUP_ID = str(uuid.uuid4())
    DEVICE_ID = str(uuid.uuid4())
    DEVICE = Devices(id=DEVICE_ID, name='Night Stand', ip_address='127.0.0.1', local_key='test', type_id='26cf7b35-8366-4c16-be9a-e0009bda62b6')
    GROUP = DeviceGroups(id=GROUP_ID, name='Bedroom', devices=[DEVICE])

    def test_map_light__should_return_correct_light_group(self):
        status = {DeviceStates.BRIGHTNESS: 500, DeviceStates.ON: True}
        actual = map_light(self.DEVICE, status)

        expected = {'lightName': self.DEVICE.name, 'lightId': str(self.DEVICE.id),
                       'groupId': str(self.DEVICE.group_id), 'on': status[DeviceStates.ON],
                       'brightness': status[DeviceStates.BRIGHTNESS]}
        assert actual == expected

    def test_map_light__should_return_zero_brightness_when_device_off(self):
        status = {DeviceStates.BRIGHTNESS: 500, DeviceStates.ON: False}
        actual = map_light(self.DEVICE, status)

        assert actual['brightness'] == 0

    def test_map_unregistered_light__should_return_light(self):
        light = UnregisteredDevices(name='Great Light', ip_address='1.1.1.1')
        actual = map_unregistered_light(light)

        assert actual['name'] == light.name
        assert actual['ipAddress'] == light.ip_address
