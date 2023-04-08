from sqlalchemy import Column, UUID, String, ForeignKey, text
from sqlalchemy.ext import declarative
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import INET

Base = declarative.declarative_base()


class DeviceTypes(Base):
    __tablename__ = 'device_types'

    id = Column(UUID, nullable=False, primary_key=True)
    name = Column(String, nullable=False)


class DeviceGroups(Base):
    __tablename__ = 'device_groups'

    id = Column(UUID, nullable=False, primary_key=True, server_default=text('gen_random_uuid()'))
    name = Column(String, nullable=False)

    devices = relationship('Devices', backref='parent', lazy='joined')


class Devices(Base):
    __tablename__ = 'devices'

    id = Column(String, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    ip_address = Column(INET, nullable=False)
    local_key = Column(String, nullable=False)
    type_id = Column(UUID, ForeignKey(DeviceTypes.id))
    group_id = Column(UUID, ForeignKey(DeviceGroups.id))

    device_type = relationship('DeviceTypes', foreign_keys='Devices.type_id')
    device_group = relationship('DeviceGroups', foreign_keys='Devices.group_id')


class UnregisteredDevices(Base):
    __tablename__ = 'unregistered_devices'

    id = Column(String, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    ip_address = Column(INET, nullable=False)
    local_key = Column(String, nullable=False)

