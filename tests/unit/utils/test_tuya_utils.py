import uuid
from unittest.mock import patch

from svc.repository.models.lights import Devices, DeviceTypes
from svc.utils.tuya_utils import set_switch, set_switch_brightness, set_switch_state, get_light_status


@patch('svc.utils.tuya_utils.tinytuya')
class TestTuyaUtils:
    DEVICE_TYPE = DeviceTypes(name='outlet')
    DEVICE = Devices(id=str(uuid.uuid4()), name='test', ip_address='127.0.0.1', local_key='tester', device_type=DEVICE_TYPE)

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

    def test_set_switch_state__should_turn_on_when_true(self, mock_tuya):
        set_switch_state(self.DEVICE, True)

        mock_tuya.OutletDevice.return_value.turn_on.assert_called()

    def test_set_switch_state__should_turn_off_when_false(self, mock_tuya):
        set_switch_state(self.DEVICE, False)

        mock_tuya.OutletDevice.return_value.turn_off.assert_called()

    def test_get_light_status__when_outlet_device_should_call_status(self, mock_tuya):
        get_light_status(self.DEVICE)

        mock_tuya.OutletDevice.return_value.status.assert_called()

    @patch('svc.utils.tuya_utils.map_light')
    def test_get_light_status__when_outlet_device_should_map_result(self, mock_map, mock_tuya):
        response = {'test': 'thing'}
        status = {'dps': response}
        mock_tuya.OutletDevice.return_value.status.return_value = status
        get_light_status(self.DEVICE)

        mock_map.assert_called_with(self.DEVICE, response)