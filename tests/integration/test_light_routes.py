import json
import uuid

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

    def test_set_light_state__should_return_success_from_service(self, mock_service):
        post_body = {'fake': 'dont matter'}

        actual = self.TEST_CLIENT.post('/lights/light/state', data=json.dumps(post_body))

        assert actual.status_code == 200

    def test_set_light_state__should_call_light_service_with_request(self, mock_service):
        body = {'groupId': 'test'}

        self.TEST_CLIENT.post('/lights/light/state', data=json.dumps(body))

        assert mock_service.update_light_state(body)

    def test_set_light_group__should_return_success_from_service(self, mock_service):
        body = {'groupId': 'test'}

        actual = self.TEST_CLIENT.post('/lights/group/state', data=json.dumps(body))

        assert actual.status_code == 200

    def test_set_light_group__should_call_light_service_with_request(self, mock_service):
        body = {'groupId': 'test'}

        self.TEST_CLIENT.post('/lights/group/state', data=json.dumps(body))

        mock_service.set_light_group.assert_called_with(body)

    def test_create_light_group__should_return_id_from_service(self, mock_service):
        body = {'name': 'doesnt matter'}
        group_id = str(uuid.uuid4())
        mock_service.create_group.return_value = group_id

        actual = self.TEST_CLIENT.post('/lights/group/create', data=json.dumps(body))

        actual.status_code = 200
        assert json.loads(actual.data) == group_id

    def test_delete_group_by_id__should_call_service(self, mock_service):
        group_id = str(uuid.uuid4())
        self.TEST_CLIENT.delete(f'/lights/group/{group_id}')

        mock_service.delete_group.assert_called_with(group_id)

    def test_delete_group_by_id__should_return_success(self, mock_service):
        group_id = str(uuid.uuid4())
        actual = self.TEST_CLIENT.delete(f'/lights/group/{group_id}')

        assert actual.status_code == 200

    def test_update_light_group__should_return_success(self, mock_service):
        request = {'groupId': str(uuid.uuid4()), 'lightId': str(uuid.uuid4())}
        actual = self.TEST_CLIENT.post('/lights/group/update', data=json.dumps(request))

        assert actual.status_code == 200

    def test_update_light_group__should_call_service_layer_with_request(self, mock_service):
        request = {'groupId': str(uuid.uuid4()), 'lightId': str(uuid.uuid4())}
        actual = self.TEST_CLIENT.post('/lights/group/update', data=json.dumps(request))

        mock_service.update_group.assert_called_with(request)
