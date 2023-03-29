import os

from svc.config.settings_state import Settings


class TestSettingsState:
    SETTINGS = None
    ENV_LIGHT_FILE = 'other.json'
    ENV_DB_NAME = 'test-db'
    ENV_DB_PORT = '3322'
    ENV_DB_USER = 'OtherUserName'
    ENV_DB_PASS = 'other_pass'

    def setup_method(self):
        self.SETTINGS = Settings.get_instance()
        os.environ.update({'LIGHT_FILE': self.ENV_LIGHT_FILE,
                           'DB_NAME': self.ENV_DB_NAME,
                           'DB_PORT': self.ENV_DB_PORT,
                           'DB_USER': self.ENV_DB_USER,
                           'DB_PASS': self.ENV_DB_PASS})

    def teardown_method(self):
        os.environ.pop('LIGHT_FILE')
        os.environ.pop('DB_NAME')
        os.environ.pop('DB_PORT')
        os.environ.pop('DB_USER')
        os.environ.pop('DB_PASS')

    def test_settings_state__should_return_light_file_from_file(self):
        test_file = 'test.json'
        self.SETTINGS.dev_mode = True
        self.SETTINGS.settings = {'lightFile': test_file}

        actual = self.SETTINGS.light_file

        assert actual == test_file

    def test_settings_state__should_return_light_file_from_env_vars(self):
        self.SETTINGS.dev_mode = False

        actual = self.SETTINGS.light_file

        assert actual == self.ENV_LIGHT_FILE

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
