import pytest

from svc.utils.file_utils import FileUtil
from werkzeug.exceptions import NotFound


class TestFileUtil:
    UTIL = None
    LIGHT_ONE = {'lightId': 1, 'lightName': 'Lamp'}
    LIGHT_TWO = {'lightId': 2, 'lightName': 'Other Lamp'}
    GROUP_ONE = {'groupId': 1, 'lights': [LIGHT_ONE]}
    GROUP_TWO = {'groupId': 2, 'lights': [LIGHT_ONE, LIGHT_TWO]}
    GROUP_THREE = {'groupId': 3, 'lights': [LIGHT_TWO]}

    def setup_method(self):
        self.UTIL = FileUtil.get_instance()

    def test_get_all_light_groups__should_return_all_registered_groups(self):
        self.UTIL.content = {'registered': [self.GROUP_TWO], 'unregistered': [self.GROUP_ONE]}
        actual = self.UTIL.get_all_light_groups()

        assert actual == [self.GROUP_TWO]

    def test_get_all_light_groups__should_raise_exception_when_no_registered_groups(self):
        self.UTIL.content = {'unregistered': []}

        with pytest.raises(NotFound):
            self.UTIL.get_all_light_groups()

    def test_get_group_by_id__should_return_matching_list(self):
        groups = [self.GROUP_ONE, self.GROUP_TWO, self.GROUP_THREE]
        self.UTIL.content = {'registered': groups, 'unregistered': []}

        actual = self.UTIL.get_group_by_id(2)

        assert actual == self.GROUP_TWO

    def test_get_group_by_id__should_raise_exception_when_no_matching_group(self):
        self.UTIL.content = {'registered': [self.GROUP_ONE]}

        with pytest.raises(NotFound):
            self.UTIL.get_group_by_id(2)