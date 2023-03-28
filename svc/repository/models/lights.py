from sqlalchemy import Column, UUID, String
from sqlalchemy.ext import declarative
from sqlalchemy.dialects.postgresql import INET

Base = declarative.declarative_base()


class DeviceTypes(Base):
    __tablename__ = 'device_types'

    id = Column(UUID, nullable=False, primary_key=True)
    name = Column(String, nullable=False)


class Devices(Base):
    __tablename__ = 'devices'

    id = Column(UUID, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    ip_address = Column(INET, nullable=False)
    local_key = Column(String, nullable=False)
    device_id = Column(String, nullable=False)