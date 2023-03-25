import json
import os

from config.file_template import template
from config.settings_state import Settings


class FileUtil:
    __instance = None
    content = None

    def __init__(self):
        if FileUtil.__instance is not None:
            raise Exception
        else:
            FileUtil.__instance = self
            FileUtil.__instance.__get_content()

    def get_all_light_groups(self):
        return self.content['registered']

    def get_group_by_id(self, group_id):
        registered_groups = self.content['registered']
        for group in registered_groups:
            if group['groupId'] == group_id:
                return group

    @staticmethod
    def __create_light_file(file_name):
        content = template
        with open(file_name, 'w+') as file:
            json.dump(content, file)
        return content

    @staticmethod
    def get_instance():
        if FileUtil.__instance is None:
            FileUtil.__instance = FileUtil()
        return FileUtil.__instance

    def __get_content(self):
        settings = Settings.get_instance()
        try:
            file_path = os.path.join(os.path.dirname(__file__), '..', '..', settings.light_file)
            with open(file_path, 'r', encoding='utf-8') as file:
                self.content = json.load(file)
        except (FileNotFoundError, TypeError):
            self.content = self.__create_light_file(settings.light_file)
