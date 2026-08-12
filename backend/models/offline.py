from sqlalchemy import Column, String, Integer
from geoalchemy2 import Geometry
from .base import Base, UUIDMixin, TimestampMixin, SyntheticMixin

class OfflinePackVersion(Base, UUIDMixin, TimestampMixin, SyntheticMixin):
    __tablename__ = 'offline_pack_versions'
    """
    Manages versions of offline map and routing data packs.
    """
    region_name = Column(String, nullable=False, index=True)
    bbox = Column(Geometry('POLYGON', srid=4326), nullable=False)
    version = Column(Integer, nullable=False)
    download_url = Column(String, nullable=False)
    size_bytes = Column(Integer, nullable=False)
