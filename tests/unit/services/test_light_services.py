from mock import patch

from svc.config.settings_state import Settings
from svc.services.light_service import get_light_groups, set_light_group


@patch('svc.services.light_service.file_utils')
class TestLightServices:
    SETTINGS = None
    FILE_CONTENTS = [{}]
    FILE_NAME = 'test.json'

    def setup_method(self):
        self.SETTINGS = Settings.get_instance()
        self.SETTINGS.dev_mode = True

    def test_get_light_groups__should_return_content_from_file(self, file_mock):
        file_mock.get_json_file.return_value = self.FILE_CONTENTS

        actual = get_light_groups()

        assert actual == self.FILE_CONTENTS

    def test_get_light_groups__should_save_file_when_does_not_exist(self, file_mock):
        self.SETTINGS.settings = {'lightFile': self.FILE_NAME}
        file_mock.get_json_file.return_value = None

        get_light_groups()

        file_mock.create_json_file.assert_called_with(self.FILE_NAME)

    def test_get_light_groups__should_return_default_file_contents(self, file_mock):
        test_file = [{'contents': 'im fake!'}]
        file_mock.get_json_file.return_value = None
        file_mock.create_json_file.return_value = test_file

        actual = get_light_groups()

        assert actual == test_file

    def test_set_light_groups__should_get_file_contents(self, mock_file):
        request = {'groupId': 'abc134', 'on': True}
        self.SETTINGS.settings = {'lightFile': self.FILE_NAME}
        set_light_group(request)

        mock_file.get_json_file.assert_called_with(self.FILE_NAME)