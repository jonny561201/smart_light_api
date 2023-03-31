import uuid

from mock import patch

from svc.config.settings_state import Settings
from svc.repository.models.lights import DeviceGroups, Devices
from svc.services.light_service import get_light_groups, set_light_group


@patch('svc.services.light_service.get_light_status')
@patch('svc.services.light_service.LightDatabaseManager')
class TestLightServices:
    SETTINGS = None
    GROUP_ID = str(uuid.uuid4())
    DEVICE_ID = str(uuid.uuid4())
    DB_DEVICE = Devices(id=DEVICE_ID, name='Lamp', ip_address='127.0.0.1', local_key='test', type_id='26cf7b35-8366-4c16-be9a-e0009bda62b6')
    DB_GROUP = DeviceGroups(id=GROUP_ID, name='Bedroom', devices=[DB_DEVICE])
    FILE_NAME = 'test.json'

    def setup_method(self):
        self.SETTINGS = Settings.get_instance()
        self.SETTINGS.dev_mode = True

    def test_get_light_groups__should_call_db_for_groups(self, mock_db, mock_status):
        mock_db.return_value.__enter__.return_value.get_light_groups.return_value = [self.DB_GROUP]

        get_light_groups()

        mock_db.return_value.__enter__.return_value.get_light_groups.assert_called()

    def test_get_light_groups__should_map_db_response(self, mock_db, mock_status):
        light = {'name': 'Lamp', 'id': self.DEVICE_ID}
        expected = [{'groupName': 'Bedroom', 'groupId': self.GROUP_ID, 'lights': [light]}]
        mock_status.return_value = light
        mock_db.return_value.__enter__.return_value.get_light_groups.return_value = [self.DB_GROUP]

        actual = get_light_groups()

        assert actual == expected

    def test_set_light_groups__should_get_groups_from_db(self, mock_db, mock_status):
        request = {'groupId': 'abc134', 'on': True}
        mock_db.return_value.__enter__.return_value.get_light_groups.return_value = [self.DB_GROUP]
        set_light_group(request)

        mock_db.return_value.__enter__.return_value.get_light_groups.assert_called()
