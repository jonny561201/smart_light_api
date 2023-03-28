import os

from svc.config.settings_state import Settings


class TestSettingsState:
    SETTINGS = None
    ENV_LIGHT_FILE = 'other.json'

    def setup_method(self):
        self.SETTINGS = Settings.get_instance()
        os.environ.update({'LIGHT_FILE': self.ENV_LIGHT_FILE})

    def teardown_method(self):
        os.environ.pop('LIGHT_FILE')

    def test_settings_state__should_return_light_file_from_file(self):
        test_file = 'test.json'
        self.SETTINGS.settings = {'lightFile': test_file}

        actual = self.SETTINGS.light_file

        assert actual == test_file

    def test_settings_state__should_return_light_file_from_env_vars(self):
        self.SETTINGS.dev_mode = False

        actual = self.SETTINGS.light_file

        assert actual == self.ENV_LIGHT_FILE