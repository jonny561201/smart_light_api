import json

from mock.mock import patch

from svc.manager import app


@patch('svc.routes.light_routes.light_service')
class TestLightRoutes:
    CONTENT = [{'test': 'fake'}]
    TEST_CLIENT = None

    def setup_method(self):
        self.TEST_CLIENT = app.test_client()

    def test_get_all_light_groups__should_return_value_from_service(self, mock_service):
        mock_service.get_light_groups.return_value = self.CONTENT

        actual = self.TEST_CLIENT.get('/lights/groups')

        assert actual.status_code == 200
        assert json.loads(actual.data) == self.CONTENT

    def test_update_light_state__should_return_success_from_service(self, mock_service):
        post_body = {'fake': 'dont matter'}

        actual = self.TEST_CLIENT.post('/lights/light/state', data=json.dumps(post_body))

        assert actual.status_code == 200
