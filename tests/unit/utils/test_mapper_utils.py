import uuid

from svc.repository.models.lights import DeviceGroups, Devices
from svc.utils.mapper_utils import map_light_groups


class TestMapperUtils:
    GROUP_ID = str(uuid.uuid4())
    DEVICE_ID = str(uuid.uuid4())
    DEVICE = Devices(id=DEVICE_ID, name='Night Stand', ip_address='127.0.0.1', local_key='test', type_id='26cf7b35-8366-4c16-be9a-e0009bda62b6')
    GROUP = DeviceGroups(id=GROUP_ID, name='Bedroom', devices=[DEVICE])

    def test_map_light_groups__should_return_correct_light_group(self):
        groups = [self.GROUP]
        actual = map_light_groups(groups)

        expected = [{'groupName': 'Bedroom', 'groupId': self.GROUP_ID, 'lights': [{'lightName': 'Night Stand', 'lightId': self.DEVICE_ID, }]}]
        assert actual == expected