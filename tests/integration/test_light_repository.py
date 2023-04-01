import uuid

from svc.repository.light_repository import LightDatabaseManager
from svc.repository.models.lights import DeviceGroups, Devices


class TestDbIntegration:
    GROUP_ONE_ID = str(uuid.uuid4())
    GROUP_TWO_ID = str(uuid.uuid4())
    DEVICE_ONE_ID = str(uuid.uuid4())
    DEVICE_TWO_ID = str(uuid.uuid4())

    GROUP_ONE = DeviceGroups(id=GROUP_ONE_ID, name='Bedroom')
    GROUP_TWO = DeviceGroups(id=GROUP_TWO_ID, name='Kitchen')
    DEVICE_ONE = Devices(id=DEVICE_ONE_ID, name='Desk Lamp', ip_address='192.0.0.121', local_key='test1', device_id=str(uuid.uuid4()), type_id='26cf7b35-8366-4c16-be9a-e0009bda62b6', device_group=GROUP_ONE)
    DEVICE_TWO = Devices(id=DEVICE_TWO_ID, name='Table Lamp', ip_address='192.0.0.120', local_key='test2', device_id=str(uuid.uuid4()), type_id='26cf7b35-8366-4c16-be9a-e0009bda62b6', device_group=GROUP_TWO)

    def setup_method(self):
        with LightDatabaseManager() as db:
            db.session.add(self.GROUP_ONE)
            db.session.add(self.GROUP_TWO)
            db.session.add(self.DEVICE_ONE)
            db.session.add(self.DEVICE_TWO)

    def teardown_method(self):
        with LightDatabaseManager() as db:
            db.session.query(Devices).delete()
            db.session.query(DeviceGroups).delete()

    def test_get_light_groups__should_return_records_from_database(self):
        with LightDatabaseManager() as db:
            actual = db.get_light_groups()

            assert str(actual[0].id) == self.GROUP_ONE_ID
            assert actual[0].name =='Bedroom'
            assert len(actual[0].devices) == 1
            assert actual[0].devices[0].name == 'Desk Lamp'

    def test_get_lights_by_group_id__should_return_records_from_database(self):
        with LightDatabaseManager() as db:
            actual = db.get_lights_by_group_id(self.GROUP_TWO_ID)

            assert len(actual) == 1
            assert actual[0].name == 'Table Lamp'
            assert actual[0].local_key == 'test2'
            assert actual[0].ip_address == '192.0.0.120'
