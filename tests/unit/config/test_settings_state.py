import os
import uuid

from svc.config.settings_state import Settings


class TestSettingsState:
    SETTINGS = None
    ENV_DB_NAME = 'test-db'
    ENV_DB_PORT = '3322'
    ENV_DB_USER = 'OtherUserName'
    ENV_DB_PASS = 'other_pass'
    ENV_API_KEY = str(uuid.uuid4())

    def setup_method(self):
        self.SETTINGS = Settings.get_instance()
        os.environ.update({'DB_NAME': self.ENV_DB_NAME,
                           'DB_PORT': self.ENV_DB_PORT,
                           'DB_USER': self.ENV_DB_USER,
                           'DB_PASS': self.ENV_DB_PASS,
                           'API_KEY': self.ENV_API_KEY})

    def teardown_method(self):
        os.environ.pop('DB_NAME')
        os.environ.pop('DB_PORT')
        os.environ.pop('DB_USER')
        os.environ.pop('DB_PASS')
        os.environ.pop('API_KEY')

    def test_settings_state__should_return_db_name_from_file(self):
        db_name = 'fake db'
        self.SETTINGS.dev_mode = True
        self.SETTINGS.settings = {'dbName': db_name}

        actual = self.SETTINGS.db_name

        assert actual == db_name

    def test_settings_state__should_return_db_name_from_env_vars(self):
        self.SETTINGS.dev_mode = False

        actual = self.SETTINGS.db_name

        assert actual == self.ENV_DB_NAME

    def test_settings_state__should_return_db_port_from_file(self):
        db_port = 4433
        self.SETTINGS.dev_mode = True
        self.SETTINGS.settings = {'dbPort': db_port}

        actual = self.SETTINGS.db_port

        assert actual == db_port

    def test_settings_state__should_return_db_port_from_env_vars(self):
        self.SETTINGS.dev_mode = False

        actual = self.SETTINGS.db_port

        assert actual == self.ENV_DB_PORT

    def test_settings_state__should_return_db_user_from_file(self):
        db_user = 'testUserName'
        self.SETTINGS.dev_mode = True
        self.SETTINGS.settings = {'dbUser': db_user}

        actual = self.SETTINGS.db_user

        assert actual == db_user

    def test_settings_state__should_return_db_user_from_env_vars(self):
        self.SETTINGS.dev_mode = False

        actual = self.SETTINGS.db_user

        assert actual == self.ENV_DB_USER

    def test_settings_state__should_return_db_pass_from_file(self):
        db_pass = 'sample_pass'
        self.SETTINGS.dev_mode = True
        self.SETTINGS.settings = {'dbPass': db_pass}

        actual = self.SETTINGS.db_pass

        assert actual == db_pass

    def test_settings_state__should_return_db_pass_from_env_vars(self):
        self.SETTINGS.dev_mode = False

        actual = self.SETTINGS.db_pass

        assert actual == self.ENV_DB_PASS

    def test_settings_state__should_return_api_key_from_file(self):
        api_key = 'sample_pass'
        self.SETTINGS.dev_mode = True
        self.SETTINGS.settings = {'apiKey': api_key}

        actual = self.SETTINGS.api_key

        assert actual == api_key

    def test_settings_state__should_return_api_keuy_from_env_vars(self):
        self.SETTINGS.dev_mode = False

        actual = self.SETTINGS.api_key

        assert actual == self.ENV_API_KEY
