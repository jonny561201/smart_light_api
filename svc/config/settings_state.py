import json
import os


class Settings:
    __instance = None
    settings = None
    dev_mode = False

    def __init__(self):
        if Settings.__instance is not None:
            raise Exception
        else:
            Settings.__instance = self
            Settings.__instance.__get_settings()

    @property
    def light_file(self):
        return self.settings.get('lightFile') if self.dev_mode else os.environ.get('LIGHT_FILE')

    @property
    def db_name(self):
        return self.settings.get('dbName') if self.dev_mode else os.environ.get('DB_NAME')

    @property
    def db_port(self):
        return self.settings.get('dbPort') if self.dev_mode else os.environ.get('DB_PORT')

    @property
    def db_user(self):
        return self.settings.get('dbUser') if self.dev_mode else os.environ.get('DB_USER')

    @property
    def db_pass(self):
        return self.settings.get('dbPass') if self.dev_mode else os.environ.get('DB_PASS')

    @property
    def api_key(self):
        return self.settings.get('apiKey') if self.dev_mode else os.environ.get('API_KEY')

    @staticmethod
    def get_instance():
        if Settings.__instance is None:
            Settings.__instance = Settings()
        return Settings.__instance

    def __get_settings(self):
        try:
            file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'settings.json')
            with open(file_path, "r") as reader:
                self.settings = json.loads(reader.read())
                self.dev_mode = self.settings.get("development", False)
        except Exception:
            self.settings = {}
