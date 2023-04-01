import uuid
from unittest.mock import patch

from svc.repository.models.lights import Devices
from svc.utils.tuya_utils import set_switch, set_switch_brightness


@patch('svc.utils.tuya_utils.tinytuya')
class TestTuyaUtils:
    DEVICE = Devices(id=str(uuid.uuid4()), name='test', ip_address='127.0.0.1', local_key='tester')

    def test_set_switch__should_turn_on_and_set_brightness_upon_request(self, mock_tuya):
        brightness = 50
        set_switch(self.DEVICE, True, brightness)

        mock_tuya.OutletDevice.return_value.turn_on.assert_called()
        mock_tuya.OutletDevice.return_value.set_value.assert_called_with(2, brightness * 10)

    def test_set_switch__should_turn_on_when_no_brightness(self, mock_tuya):
        set_switch(self.DEVICE, True, None)

        mock_tuya.OutletDevice.return_value.turn_on.assert_called()
        mock_tuya.OutletDevice.return_value.set_value.assert_not_called()

    def test_set_switch__should_turn_off_when_requested(self, mock_tuya):
        set_switch(self.DEVICE, False, None)

        mock_tuya.OutletDevice.return_value.turn_off.assert_called()
        mock_tuya.OutletDevice.return_value.set_value.assert_not_called()


    def test_set_switch_brightness__should_turn_off_when_brightness_is_zero(self, mock_tuya):
        set_switch_brightness(self.DEVICE, 0)

        mock_tuya.OutletDevice.return_value.turn_off.assert_called()


    def test_set_switch_brightness__should_turn_on_when_brightness_greater_than_zero(self, mock_tuya):
        set_switch_brightness(self.DEVICE, 10)

        mock_tuya.OutletDevice.return_value.turn_on.assert_called()


    def test_set_switch_brightness__should_set_value_when_brightness_greater_than_zero(self, mock_tuya):
        set_switch_brightness(self.DEVICE, 60)

        mock_tuya.OutletDevice.return_value.set_value.assert_called_with(2, 60 * 10)