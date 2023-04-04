import uuid

from mock import patch

from svc.repository.models.lights import DeviceGroups, Devices
from svc.services.light_service import get_light_groups, set_light_group, create_group, delete_group


@patch('svc.services.light_service.tuya_utils')
@patch('svc.services.light_service.LightDatabaseManager')
class TestLightServices:
    GROUP_ID = str(uuid.uuid4())
    DEVICE_ONE_ID = str(uuid.uuid4())
    DEVICE_TWO_ID = str(uuid.uuid4())
    DEVICE_ONE = Devices(id=DEVICE_ONE_ID, name='Lamp', ip_address='127.0.0.1', local_key='test', type_id='26cf7b35-8366-4c16-be9a-e0009bda62b6')
    DEVICE_TWO = Devices(id=DEVICE_TWO_ID, name='Lamp', ip_address='127.0.0.1', local_key='test', type_id='26cf7b35-8366-4c16-be9a-e0009bda62b6')
    DB_GROUP = DeviceGroups(id=GROUP_ID, name='Bedroom', devices=[DEVICE_ONE])

    def test_get_light_groups__should_call_db_for_groups(self, mock_db, mock_tuya):
        mock_db.return_value.__enter__.return_value.get_light_groups.return_value = [self.DB_GROUP]

        get_light_groups()

        mock_db.return_value.__enter__.return_value.get_light_groups.assert_called()

    def test_get_light_groups__should_map_db_response(self, mock_db, mock_tuya):
        light = {'name': 'Lamp', 'id': self.DEVICE_ONE_ID, 'on': True, 'brightness': 50}
        expected = [{'groupName': 'Bedroom', 'groupId': self.GROUP_ID, 'lights': [light], 'on': True, 'brightness': 50}]
        mock_tuya.get_light_status.return_value = light
        mock_db.return_value.__enter__.return_value.get_light_groups.return_value = [self.DB_GROUP]

        actual = get_light_groups()

        assert actual == expected

    def test_get_light_groups__should_set_on_and_brightness_to_default_when_zero_lights_returned(self, mock_db, mock_tuya):
        group = DeviceGroups(id=self.GROUP_ID, name='Bedroom', devices=[])
        mock_db.return_value.__enter__.return_value.get_light_groups.return_value = [group]
        mock_tuya.get_light_status.return_value = []

        actual = get_light_groups()

        assert actual[0]['on'] == False
        assert actual[0]['brightness'] == 0

    def test_set_light_groups__should_get_groups_from_db(self, mock_db, mock_tuya):
        request = {'groupId': 'abc134', 'on': True}
        mock_db.return_value.__enter__.return_value.get_lights_by.return_value = [self.DB_GROUP]
        set_light_group(request)

        mock_db.return_value.__enter__.return_value.get_lights_by.assert_called()

    def test_set_light_groups__should_set_state_of_all_lights_in_group(self, mock_db, mock_tuya):
        request = {'groupId': 'abc134', 'on': True, 'brightness': 50}
        mock_db.return_value.__enter__.return_value.get_lights_by.return_value = [self.DEVICE_ONE, self.DEVICE_TWO]

        set_light_group(request)

        mock_tuya.set_switch.assert_any_call(self.DEVICE_ONE, request['on'], request['brightness'])
        mock_tuya.set_switch.assert_any_call(self.DEVICE_TWO, request['on'], request['brightness'])

    def test_create_group__should_call_repository_with_name(self, mock_db, mock_tuya):
        request = {'name': 'test name'}

        create_group(request)

        mock_db.return_value.__enter__.return_value.create_new_group.assert_called_with(request['name'])

    def test_create_group__should_return_response_from_repository(self, mock_db, mock_tuya):
        request = {'name': 'test'}
        group_id = str(uuid.uuid4())
        mock_db.return_value.__enter__.return_value.create_new_group.return_value = group_id

        actual = create_group(request)

        assert actual == group_id

    def test_delete_group__should_call_database_method_to_delete(self, mock_db, mock_tuya):
        group_id = str(uuid.uuid4())
        delete_group(group_id)

        mock_db.return_value.__enter__.return_value.delete_group_by.assert_called_with(group_id)