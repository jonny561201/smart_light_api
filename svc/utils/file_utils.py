import json


def get_json_file(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, TypeError):
        return


def create_json_file(file_name):
    content = [{'groupId': 1, 'groupName': 'Living Room', 'brightness': 100, 'on': True, 'lights': [
        {'brightness': 80, 'lightName': 'lamp', 'lightId': 2, 'groupId': 1, 'on': True},
        {'brightness': 10, 'lightName': 'desk', 'lightId': 3, 'groupId': 1, 'on': True},
    ]}]
    with open(file_name, 'w+') as file:
        json.dump(content, file)
    return content
