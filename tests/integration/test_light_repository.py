import uuid
from unittest.mock import patch

from svc.repository.light_repository import LightDatabaseManager
from svc.repository.models.lights import DeviceGroups, Devices, UnregisteredDevices


class TestDbIntegration:
    GROUP_ONE_ID = str(uuid.uuid4())
    GROUP_TWO_ID = str(uuid.uuid4())
    ID_ONE = str(uuid.uuid4())
    ID_TWO = str(uuid.uuid4())

    GROUP_ONE = DeviceGroups(id=GROUP_ONE_ID, name='Bedroom')
    GROUP_TWO = DeviceGroups(id=GROUP_TWO_ID, name='Kitchen')
    DEVICE_ONE = Devices(id=ID_ONE, name='Desk Lamp', ip_address='192.0.0.121', local_key='test1', type_id='26cf7b35-8366-4c16-be9a-e0009bda62b6', device_group=GROUP_ONE)
    DEVICE_TWO = Devices(id=ID_TWO, name='Table Lamp', ip_address='192.0.0.120', local_key='test2', type_id='26cf7b35-8366-4c16-be9a-e0009bda62b6', device_group=GROUP_TWO)

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
            db.session.query(UnregisteredDevices).delete()

    def test_get_light_groups__should_return_records_from_database(self):
        with LightDatabaseManager() as db:
            actual = db.get_light_groups()

            assert str(actual[0].id) == self.GROUP_ONE_ID
            assert actual[0].name =='Bedroom'
            assert len(actual[0].devices) == 1
            assert actual[0].devices[0].name == 'Desk Lamp'

    def test_get_light_by__should_return_single_matching_device(self):
        with LightDatabaseManager() as db:
            actual = db.get_light_by(self.ID_TWO)

            assert actual.name == 'Table Lamp'
            assert actual.ip_address == '192.0.0.120'

    def test_get_all_lights__should_return_all_devices(self):
        with LightDatabaseManager() as db:
            actual = db.get_all_lights()

            assert str(actual[0].id) == self.ID_ONE
            assert str(actual[1].id) == self.ID_TWO

    def test_get_unregistered_light_by__should_return_record_from_database(self):
        id = str(uuid.uuid4())
        unregistered = UnregisteredDevices(id=id, name='test', ip_address='192.1.1.1', local_key='key test')
        with LightDatabaseManager() as db:
            db.session.add(unregistered)

        with LightDatabaseManager() as db:
            actual = db.get_unregistered_light_by(id)
            assert actual.id == id

    def test_get_all_unregistered_lights__should_return_records(self):
        id = str(uuid.uuid4())
        unregistered = UnregisteredDevices(id=id, name='test', ip_address='192.1.1.1', local_key='key test')

        with LightDatabaseManager() as db:
            db.session.add(unregistered)

        with LightDatabaseManager() as db:
            actual = db.get_all_unregistered_lights()
            assert actual[0].id == id

    def test_get_lights_by_group_id__should_return_records_from_database(self):
        with LightDatabaseManager() as db:
            actual = db.get_lights_by(self.GROUP_TWO_ID)

            assert len(actual) == 1
            assert actual[0].name == 'Table Lamp'
            assert actual[0].local_key == 'test2'
            assert actual[0].ip_address == '192.0.0.120'

    def test_insert_unregistered_devices__should_insert_records(self):
        device_one = {'name': 'test1', 'ip': '127.0.0.1', 'id': '87asyds23', 'key': '234SAHDF'}
        device_two = {'name': 'test2', 'ip': '127.0.0.2', 'id': '549ADSF87', 'key': '657DFA58'}
        devices = [device_one, device_two]
        with LightDatabaseManager() as db:
            db.insert_unregistered_devices(devices)

        with LightDatabaseManager() as db:
            actual = db.session.query(UnregisteredDevices).all()

            assert len(actual) == 2
            assert actual[0].name == device_one['name']
            assert actual[1].name == device_two['name']

    def test_create_new_group__should_insert_new_group_record(self):
        name = 'my fake room'
        with LightDatabaseManager() as db:
            db.create_new_group(name)

        with LightDatabaseManager() as db:
            actual = db.session.query(DeviceGroups).filter_by(name=name).first()

            assert actual.name == name

    @patch('svc.repository.light_repository.uuid')
    def test_create_new_group__should_return_new_group_id(self, mock_uuid):
        new_key = uuid.uuid4()
        mock_uuid.uuid4.return_value = new_key

        with LightDatabaseManager() as db:
            actual = db.create_new_group('test name')

            assert actual == new_key

    def test_delete_group__should_remove_group_by_id(self):
        with LightDatabaseManager() as db:
            db.delete_group_by(self.GROUP_TWO_ID)

        with LightDatabaseManager() as db:
            actual = db.session.query(DeviceGroups).filter_by(id=self.GROUP_TWO_ID).first()
            light = db.session.query(Devices).filter_by(id=self.ID_TWO).first()
            assert actual is None
            assert str(light.id) == self.ID_TWO

    def test_update_light_group__should_update_devices_group_id(self):
        with LightDatabaseManager() as db:
            db.update_light_group(self.ID_ONE, self.GROUP_TWO_ID)

        with LightDatabaseManager() as db:
            actual = db.session.query(Devices).filter_by(id=self.ID_ONE).first()
            assert str(actual.group_id) == self.GROUP_TWO_ID

    def test_update_light_group__should_set_group_id_to_null(self):
        with LightDatabaseManager() as db:
            db.update_light_group(self.ID_TWO, None)

        with LightDatabaseManager() as db:
            actual = db.session.query(Devices).filter_by(id=self.ID_TWO).first()
            assert actual.group_id is None

    def test_get_unassigned_light_by__should_return_all_lights_without_group(self):
        device = Devices(id=str(uuid.uuid4()), name='Unassigned', ip_address='192.1.1.1', local_key='doesnt matter', type_id='26cf7b35-8366-4c16-be9a-e0009bda62b6', group_id=None)
        with LightDatabaseManager() as db:
            db.session.add(device)

        with LightDatabaseManager() as db:
            actual = db.get_unassigned_lights()

            assert len(actual) == 1
            assert actual[0].name == 'Unassigned'
            assert actual[0].ip_address == '192.1.1.1'

