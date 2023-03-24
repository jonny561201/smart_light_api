from mock import patch

from svc.config.settings_state import Settings
from svc.services.light_service import get_light_groups


@patch('svc.services.light_service.file_utils')
class TestLightServices:
    SETTINGS = None
    FILE_CONTENTS = [{}]

    def setup_method(self):
        self.SETTINGS = Settings.get_instance()
        self.SETTINGS.dev_mode = True

    def test_get_light_groups__should_return_content_from_file(self, file_mock):
        file_mock.get_json_file.return_value = self.FILE_CONTENTS

        actual = get_light_groups()

        assert actual == self.FILE_CONTENTS

    def test_get_light_groups__should_save_file_when_does_not_exist(self, file_mock):
        file_name = 'test.json'
        self.SETTINGS.settings = {'lightFile': file_name}
        file_mock.get_json_file.return_value = None

        get_light_groups()

        file_mock.save_json_file.assert_called_with(file_name)

    def test_get_light_groups__should_return_default_file_contents(self, file_mock):
        test_file = [{'contents': 'im fake!'}]
        file_mock.get_json_file.return_value = None
        file_mock.save_json_file.return_value = test_file

        actual = get_light_groups()

        assert actual == test_file