import json

from mock.mock import patch

from svc.routes.light_routes import get_all_light_groups


@patch('svc.routes.light_routes.light_service')
def test_get_all_light_groups__should_return_value_from_service(mock_service):
    content = [{'test': 'fake'}]
    mock_service.get_light_groups.return_value = content

    actual = get_all_light_groups()

    assert actual.status == '200 OK'
    assert json.loads(actual.data) == content
