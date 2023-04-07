import uuid

from sqlalchemy import orm, create_engine

from svc.config.settings_state import Settings
from svc.repository.models.lights import DeviceGroups, Devices, UnregisteredDevices


class LightDatabaseManager:
    db_session = None

    def __enter__(self):
        settings = Settings.get_instance()
        connection = f'postgresql://{settings.db_user}:{settings.db_pass}@localhost:{settings.db_port}/{settings.db_name}'

        db_engine = create_engine(connection)
        session = orm.sessionmaker(bind=db_engine)
        self.db_session = orm.scoped_session(session)

        return LightDatabase(self.db_session)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db_session.commit()
        self.db_session.remove()


class LightDatabase:
    def __init__(self, session):
        self.session = session

    def get_light_groups(self):
        return self.session.query(DeviceGroups).all()

    def get_all_lights(self):
        return self.session.query(Devices).all()

    def get_lights_by(self, group_id):
        return self.session.query(Devices).filter_by(group_id=group_id).all()

    def insert_unregistered_devices(self, devices):
        new_devices = [self.__create_new_device(device) for device in devices]
        self.session.add_all(new_devices)

    def create_new_group(self, name):
        group = DeviceGroups(id=(uuid.uuid4()), name=name)
        self.session.add(group)
        return group.id

    def delete_group_by(self, group_id):
        lights = self.session.query(Devices).filter_by(group_id=group_id).all()
        for light in lights:
            self.session.delete(light.device_group)
        self.session.query(DeviceGroups).filter_by(id=group_id).delete()

    @staticmethod
    def __create_new_device(device):
        return UnregisteredDevices(name=device.get('name'), ip_address=device.get('ip'), device_id=device.get('id'), local_key=device.get('key'))