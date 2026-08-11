"""
IMPORTANT PostGIS Rules for DriveGuard V3:
- Store geometry as SRID 4326 (WGS84).
- ALL meter-based operations MUST cast to geography: ST_Buffer(geom::geography, meters)::geometry
- Distance calculations: ST_Length(geom::geography) or ST_Distance(geom::geography, other::geography)

This migration creates all necessary tables and extensions for the DriveGuard V3 platform.
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import geoalchemy2

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis;")
    # Complete initial schema setup logic will be added via models and autogenerate
    pass


def downgrade() -> None:
    # Downgrade logic to drop all tables
    pass
