import uuid
from unittest.mock import patch

import pytest
from werkzeug.exceptions import Unauthorized

from config.settings_state import Settings
from utils.api_utils import is_valid


@patch('svc.utils.api_utils.Settings')
class TestApiUtils:
    API_KEY = str(uuid.uuid4())

    def setup_method(self):
        self.SETTINGS = Settings.get_instance()
        self.SETTINGS.settings = {'apiKey': self.API_KEY}

    def test_is_valid__should_return_none_when_key_valid(self, mock_setting):
        mock_setting.get_instance.return_value = self.SETTINGS
        actual = is_valid(self.API_KEY)

        assert actual is None

    def test_is_valid__should_raise_unauthorized_when_keys_mismatch(self, mock_setting):
        mock_setting.get_instance.return_value = self.SETTINGS
        with pytest.raises(Unauthorized):
            is_valid('bad key')

