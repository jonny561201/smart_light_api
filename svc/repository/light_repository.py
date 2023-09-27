import uuid

from sqlalchemy import orm, create_engine

from svc.config.settings_state import Settings
from svc.config.tuya_constants import TuyaTypes
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

    # def get_moar_light_groups(self):
    #     groups = self.session.query(DeviceGroups).all()
    #     return list(map(self.__map_group, groups))

    def get_light_by(self, light_id):
        return self.session.query(Devices).filter_by(id=light_id).first()

    def get_all_lights(self):
        return self.session.query(Devices).all()

    def get_lights_by(self, group_id):
        return self.session.query(Devices).filter_by(group_id=group_id).all()

    def get_unregistered_light_by(self, light_id):
        return self.session.query(UnregisteredDevices).filter_by(id=light_id).first()

    def get_all_unregistered_lights(self):
        return self.session.query(UnregisteredDevices).all()

    def delete_unregistered_light_by(self, unregistered):
        self.session.delete(unregistered)

    def update_light_group(self, light_id, group_id):
        light = self.session.query(Devices).filter_by(id=light_id).first()
        light.group_id = group_id

    def insert_unregistered_devices(self, devices):
        new_devices = [self.__map_new_device(device) for device in devices]
        for device in new_devices:
            self.session.merge(device)
        return new_devices

    def assign_new_light(self, unregistered_light, group_id, name, switch_type_id):
        light = Devices(id=unregistered_light.id, name=name, ip_address=unregistered_light.ip_address, local_key=unregistered_light.local_key, group_id=group_id, type_id=TuyaTypes.OUTLET, switch_type_id=switch_type_id)
        self.session.add(light)

    def create_new_group(self, name):
        group = DeviceGroups(id=(uuid.uuid4()), name=name)
        self.session.add(group)
        return str(group.id)

    def delete_group_by(self, group_id):
        lights = self.session.query(Devices).filter_by(group_id=group_id).all()
        for light in lights:
            self.session.delete(light.device_group)
        self.session.query(DeviceGroups).filter_by(id=group_id).delete()

    @staticmethod
    def __map_new_device(device):
        return UnregisteredDevices(name=device.get('name'), ip_address=device.get('ip'), id=device.get('id'), local_key=device.get('key'))

    # @staticmethod
    # def __map_group(group):
    #     devices = list(map(LightDatabase.__map_light, group.devices))
    #     return {
    #         'id': str(group.id),
    #         'name': group.name,
    #         'devices': devices
    #     }
    #
    # @staticmethod
    # def __map_light(light):
    #     return {
    #         'id': str(light.id),
    #         'name': light.name,
    #         'ipAddress': light.ip_address,
    #         'localKey': light.local_key,
    #         'deviceId': light.device_id,
    #         'groupId': light.group_id
    #     }
