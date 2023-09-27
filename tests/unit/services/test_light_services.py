import uuid

from mock import patch

from svc.repository.models.lights import DeviceGroups, Devices, UnregisteredDevices
from svc.services.light_service import get_light_groups, set_light_group, create_group, delete_group, \
    scan_unregistered_devices, assign_group, update_group, update_light_state, get_unregistered_devices


@patch('svc.services.light_service.map_unregistered_light')
@patch('svc.services.light_service.is_valid')
@patch('svc.services.light_service.tuya_utils')
@patch('svc.services.light_service.LightDatabaseManager')
class TestLightServices:
    API_KEY = str(uuid.uuid4())
    GROUP_ID = str(uuid.uuid4())
    DEVICE_ONE_ID = str(uuid.uuid4())
    DEVICE_TWO_ID = str(uuid.uuid4())
    DEVICE_ONE = Devices(id=DEVICE_ONE_ID, name='Lamp', ip_address='127.0.0.1', local_key='test', type_id='26cf7b35-8366-4c16-be9a-e0009bda62b6')
    DEVICE_TWO = Devices(id=DEVICE_TWO_ID, name='Lamp', ip_address='127.0.0.1', local_key='test', type_id='26cf7b35-8366-4c16-be9a-e0009bda62b6')
    DB_GROUP = DeviceGroups(id=GROUP_ID, name='Bedroom', devices=[DEVICE_ONE])

    def test_get_light_groups__should_call_db_for_groups(self, mock_db, mock_tuya, mock_api, mock_map):
        mock_db.return_value.__enter__.return_value.get_light_groups.return_value = [self.DB_GROUP]

        get_light_groups(self.API_KEY)

        mock_db.return_value.__enter__.return_value.get_light_groups.assert_called()

    def test_get_light_groups__should_validate_api_key(self, mock_db, mock_tuya, mock_api, mock_map):
        get_light_groups(self.API_KEY)

        mock_api.assert_called_with(self.API_KEY)

    def test_get_light_groups__should_map_db_response(self, mock_db, mock_tuya, mock_api, mock_map):
        light = {'name': 'Lamp', 'id': self.DEVICE_ONE_ID, 'on': True, 'brightness': 50}
        expected = [{'groupName': 'Bedroom', 'groupId': self.GROUP_ID, 'lights': [light], 'on': True, 'brightness': 50}]
        mock_tuya.get_light_status.return_value = light
        mock_db.return_value.__enter__.return_value.get_light_groups.return_value = [self.DB_GROUP]

        actual = get_light_groups(self.API_KEY)

        assert actual == expected

    def test_get_light_groups__should_set_on_and_brightness_to_default_when_zero_lights_returned(self, mock_db, mock_tuya, mock_api, mock_map):
        group = DeviceGroups(id=self.GROUP_ID, name='Bedroom', devices=[])
        mock_db.return_value.__enter__.return_value.get_light_groups.return_value = [group]
        mock_tuya.get_light_status.return_value = []

        actual = get_light_groups(self.API_KEY)

        assert actual[0]['on'] is False
        assert actual[0]['brightness'] == 0

    def test_update_light_state__should_validate_api_key(self, mock_db, mock_tuya, mock_api, mock_map):
        request = {'lightId': self.DEVICE_ONE_ID}
        update_light_state(self.API_KEY, request)

        mock_api.assert_called_with(self.API_KEY)

    def test_update_light_state__should_call_db_for_light_by_id(self, mock_db, mock_tuya, mock_api, mock_map):
        request = {'lightId': self.DEVICE_ONE_ID}
        update_light_state(self.API_KEY, request)

        mock_db.return_value.__enter__.return_value.get_light_by.assert_called_with(self.DEVICE_ONE_ID)

    def test_update_light_state__should_set_tuya_switch(self, mock_db, mock_tuya, mock_api, mock_map):
        request = {'lightId': self.DEVICE_ONE_ID, 'on': True, 'brightness': 50}
        mock_db.return_value.__enter__.return_value.get_light_by.return_value = self.DEVICE_ONE
        update_light_state(self.API_KEY, request)

        mock_tuya.set_switch.assert_called_with(self.DEVICE_ONE, request['on'], request['brightness'])

    def test_set_light_groups__should_validate_api_key(self, mock_db, mock_tuya, mock_api, mock_map):
        request = {'groupId': 'abc134', 'on': True}
        mock_db.return_value.__enter__.return_value.get_lights_by.return_value = [self.DB_GROUP]
        set_light_group(self.API_KEY, request)

        mock_api.assert_called_with(self.API_KEY)

    def test_set_light_groups__should_get_groups_from_db(self, mock_db, mock_tuya, mock_api, mock_map):
        request = {'groupId': 'abc134', 'on': True}
        mock_db.return_value.__enter__.return_value.get_lights_by.return_value = [self.DB_GROUP]
        set_light_group(self.API_KEY, request)

        mock_db.return_value.__enter__.return_value.get_lights_by.assert_called()

    def test_set_light_groups__should_set_state_of_all_lights_in_group(self, mock_db, mock_tuya, mock_api, mock_map):
        request = {'groupId': 'abc134', 'on': True, 'brightness': 50}
        mock_db.return_value.__enter__.return_value.get_lights_by.return_value = [self.DEVICE_ONE, self.DEVICE_TWO]

        set_light_group(self.API_KEY, request)

        mock_tuya.set_switch.assert_any_call(self.DEVICE_ONE, request['on'], request['brightness'])
        mock_tuya.set_switch.assert_any_call(self.DEVICE_TWO, request['on'], request['brightness'])

    def test_create_group__should_validate_api_call(self, mock_db, mock_tuya, mock_api, mock_map):
        request = {'name': 'test name'}

        create_group(self.API_KEY, request)

        mock_api.assert_called_with(self.API_KEY)

    def test_create_group__should_call_repository_with_name(self, mock_db, mock_tuya, mock_api, mock_map):
        request = {'name': 'test name'}

        create_group(self.API_KEY, request)

        mock_db.return_value.__enter__.return_value.create_new_group.assert_called_with(request['name'])

    def test_create_group__should_return_response_from_repository(self, mock_db, mock_tuya, mock_api, mock_map):
        request = {'name': 'test'}
        group_id = str(uuid.uuid4())
        mock_db.return_value.__enter__.return_value.create_new_group.return_value = group_id

        actual = create_group(self.API_KEY, request)

        assert actual == group_id

    def test_delete_group__should_call_database_method_to_delete(self, mock_db, mock_tuya, mock_api, mock_map):
        group_id = str(uuid.uuid4())
        delete_group(self.API_KEY, group_id)

        mock_db.return_value.__enter__.return_value.delete_group_by.assert_called_with(group_id)

    def test_delete_group__should_validate_api_key(self, mock_db, mock_tuya, mock_api, mock_map):
        group_id = str(uuid.uuid4())
        delete_group(self.API_KEY, group_id)

        mock_api.assert_called_with(self.API_KEY)

    def test_scan_unregistered_devices__should_validate_api_key(self, mock_db, mock_tuya, mock_api, mock_map):
        scan_unregistered_devices(self.API_KEY)

        mock_api.assert_called_with(self.API_KEY)

    def test_scan_unregistered_devices__should_query_tuya_devices_scan(self, mock_db, mock_tuya, mock_api, mock_map):
        scan_unregistered_devices(self.API_KEY)

        mock_tuya.scan_for_devices.assert_called()

    def test_scan_unregistered_devices__should_compare_devices_from_scan_and_database(self, mock_db, mock_tuya, mock_api, mock_map):
        device_id = '1234'
        expected_device = {'id': '234235'}
        mock_tuya.scan_for_devices.return_value = [{'id': device_id}, expected_device]
        device_one = Devices(id=device_id)
        mock_db.return_value.__enter__.return_value.get_all_lights.return_value = [device_one]

        actual = scan_unregistered_devices(self.API_KEY)

        assert actual == [expected_device]

    def test_get_unregistered_devices__should_validate_api_key(self, mock_db, mock_tuya, mock_api, mock_map):
        get_unregistered_devices(self.API_KEY)

        mock_api.assert_called_with(self.API_KEY)

    def test_get_unregistered_devices__should_query_devices_from_db(self, mock_db, mock_tuya, mock_api, mock_map):
        get_unregistered_devices(self.API_KEY)

        mock_db.return_value.__enter__.return_value.get_unregistered_lights.assert_called()

    def test_get_unregistered_devices__should_return_devices_from_db(self, mock_db, mock_tuya, mock_api, mock_map):
        devices = [UnregisteredDevices(name='test')]
        map_device = {'name': 'Test Name', 'ipAddress': '0.0.0.0'}

        mock_map.return_value = map_device
        mock_db.return_value.__enter__.return_value.get_unregistered_lights.return_value = devices

        actual = get_unregistered_devices(self.API_KEY)

        assert actual == [map_device]

    def test_assign_group__should_validate_api_key(self, mock_db, mock_tuya, mock_api, mock_map):
        request = {'lightId': 1, 'groupId': str(uuid.uuid4())}

        assign_group(self.API_KEY, request)

        mock_api.assert_called_with(self.API_KEY)

    def test_assign_group__should_scan_unregistered_devices_by_id(self, mock_db, mock_tuya, mock_api, mock_map):
        request = {'lightId': 1, 'groupId': str(uuid.uuid4())}

        assign_group(self.API_KEY, request)

        mock_db.return_value.__enter__.return_value.get_unregistered_light_by.assert_called_with(request['lightId'])

    def test_assign_group__should_call_to_assign_new_light(self, mock_db, mock_tuya, mock_api, mock_map):
        request = {'lightId': 1, 'groupId': str(uuid.uuid4()), 'name': 'testName', 'switchTypeId': 3}
        device = UnregisteredDevices()
        mock_db.return_value.__enter__.return_value.get_unregistered_light_by.return_value = device

        assign_group(self.API_KEY, request)

        mock_db.return_value.__enter__.return_value.assign_new_light.assert_called_with(device, request['groupId'], request['name'], request['switchTypeId'])

    def test_assign_group__should_delete_unregistered_device(self, mock_db, mock_tuya, mock_api, mock_map):
        request = {'lightId': 1, 'groupId': str(uuid.uuid4())}
        device = UnregisteredDevices()
        mock_db.return_value.__enter__.return_value.get_unregistered_light_by.return_value = device

        assign_group(self.API_KEY, request)

        mock_db.return_value.__enter__.return_value.delete_unregistered_light_by.assert_called_with(device)

    def test_update_group__should_validate_api_key(self, mock_db, mock_tuya, mock_api, mock_map):
        request = {'lightId': 1, 'groupId': str(uuid.uuid4())}

        update_group(self.API_KEY, request)

        mock_api.assert_called_with(self.API_KEY)

    def test_update_group__should_call_to_update_light_group_with_request(self, mock_db, mock_tuya, mock_api, mock_map):
        request = {'lightId': 1, 'groupId': str(uuid.uuid4())}

        update_group(self.API_KEY, request)

        mock_db.return_value.__enter__.return_value.update_light_group.assert_called_with(request['lightId'], request['groupId'])
