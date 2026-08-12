from geoalchemy2 import Geometry
from sqlalchemy import Column, ForeignKey, String

from .base import Base, SyntheticMixin, TimestampMixin, UUIDMixin


class FavoritePlace(Base, UUIDMixin, TimestampMixin, SyntheticMixin):
    __tablename__ = 'favorite_places'
    """
    User's favorite places (Home, Work, etc).
    """
    user_id = Column(ForeignKey('users.id'), nullable=False, index=True)
    name = Column(String, nullable=False)
    location = Column(Geometry('POINT', srid=4326), nullable=False)

class RecentPlace(Base, UUIDMixin, TimestampMixin, SyntheticMixin):
    __tablename__ = 'recent_places'
    """
    Recently visited or searched places.
    """
    user_id = Column(ForeignKey('users.id'), nullable=False, index=True)
    name = Column(String, nullable=False)
    location = Column(Geometry('POINT', srid=4326), nullable=False)
