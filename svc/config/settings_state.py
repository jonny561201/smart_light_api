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
                self.dev_mode = self.settings.get("environment", False)
        except Exception:
            self.settings = {}