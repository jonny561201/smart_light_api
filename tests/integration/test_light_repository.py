import uuid

from svc.repository.light_repository import LightDatabaseManager
from svc.repository.models.lights import DeviceGroups, Devices


class TestDbIntegration:

    GROUP_ID = str(uuid.uuid4())
    DEVICE_ID = str(uuid.uuid4())
    GROUP = DeviceGroups(id=GROUP_ID, name='Bedroom')
    DEVICE = Devices(id=DEVICE_ID, name='Desk Lamp', ip_address='192.0.0.121', local_key='test', device_id=str(uuid.uuid4()), type_id='26cf7b35-8366-4c16-be9a-e0009bda62b6', device_group=GROUP)

    def setup_method(self):
        with LightDatabaseManager() as db:
            db.session.add(self.GROUP)
            db.session.add(self.DEVICE)

    def teardown_method(self):
        with LightDatabaseManager() as db:
            db.session.query(Devices).delete()
            db.session.query(DeviceGroups).delete()

    def test_get_light_groups__should_return_records_from_database(self):
        with LightDatabaseManager() as db:
            actual = db.get_light_groups()

            assert str(actual[0].id) == self.GROUP_ID
            assert actual[0].name =='Bedroom'
            assert len(actual[0].devices) == 1
            assert actual[0].devices[0].name == 'Desk Lamp'
