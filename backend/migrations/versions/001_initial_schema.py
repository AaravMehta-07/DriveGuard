"""
Initial PostGIS and DriveGuard V3 Complete Production Schema

Revision ID: 001
Revises: None
Create Date: 2026-08-11

IMPORTANT PostGIS Rules for DriveGuard V3:
- Store geometry as SRID 4326 (WGS84).
- ALL meter-based operations MUST cast to geography: ST_Buffer(geom::geography, meters)::geometry
- Distance calculations: ST_Length(geom::geography) or ST_Distance(geom::geography, other::geography)
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import geoalchemy2

revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. PostGIS Extension
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis;")

    # 2. Users Table
    op.create_table(
        'users',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('email', sa.String(255), unique=True, nullable=True),
        sa.Column('display_name', sa.String(255), nullable=True),
        sa.Column('is_anonymous', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('role', sa.String(32), server_default='USER', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
    )

    # 3. User Preferences
    op.create_table(
        'user_preferences',
        sa.Column('user_id', sa.String(64), sa.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('voice_alerts_enabled', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('haptics_enabled', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('overspeed_warning_threshold_kph', sa.Integer(), server_default='5', nullable=False),
        sa.Column('theme_mode', sa.String(32), server_default='DARK', nullable=False),
        sa.Column('vehicle_class', sa.String(32), server_default='LMV', nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
    )

    # 4. Data Sources Table
    op.create_table(
        'data_sources',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('source_type', sa.String(64), nullable=False),
        sa.Column('trust_score', sa.Float(), server_default='0.5', nullable=False),
        sa.Column('persistent_storage_allowed', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('overlay_allowed', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('cross_provider_display_allowed', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
    )

    # 5. Enforcement Points Table
    op.create_table(
        'enforcement_points',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('source_id', sa.String(64), sa.ForeignKey('data_sources.id'), nullable=False),
        sa.Column('enforcement_type', sa.String(64), nullable=False),
        sa.Column('verification_status', sa.String(32), server_default='UNVERIFIED', nullable=False),
        sa.Column('speed_limit_kph', sa.Integer(), nullable=True),
        sa.Column('direction_heading', sa.Float(), nullable=True),
        sa.Column('road_name', sa.String(255), nullable=True),
        sa.Column('road_level', sa.Integer(), server_default='0', nullable=False),
        sa.Column('location', geoalchemy2.Geometry('POINT', srid=4326), nullable=False),
        sa.Column('synthetic', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
    )
    op.execute("CREATE INDEX IF NOT EXISTS idx_enforcement_points_location ON enforcement_points USING GIST (location);")

    # 6. Road Segments Table
    op.create_table(
        'road_segments',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('name', sa.String(255), nullable=True),
        sa.Column('speed_limit_kph', sa.Integer(), nullable=True),
        sa.Column('road_level', sa.Integer(), server_default='0', nullable=False),
        sa.Column('is_one_way', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('geometry', geoalchemy2.Geometry('LINESTRING', srid=4326), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
    )
    op.execute("CREATE INDEX IF NOT EXISTS idx_road_segments_geometry ON road_segments USING GIST (geometry);")

    # 7. Speed Limits Table
    op.create_table(
        'speed_limits',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('segment_id', sa.String(64), sa.ForeignKey('road_segments.id'), nullable=False),
        sa.Column('speed_limit_kph', sa.Integer(), nullable=False),
        sa.Column('vehicle_class', sa.String(32), server_default='ALL', nullable=False),
        sa.Column('start_time', sa.Time(), nullable=True),
        sa.Column('end_time', sa.Time(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
    )

    # 8. Traffic Signals Table
    op.create_table(
        'traffic_signal_junctions',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('junction_name', sa.String(255), nullable=False),
        sa.Column('has_red_light_camera', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('location', geoalchemy2.Geometry('POINT', srid=4326), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
    )
    op.execute("CREATE INDEX IF NOT EXISTS idx_traffic_signals_location ON traffic_signal_junctions USING GIST (location);")

    # 9. Turn Restrictions Table
    op.create_table(
        'turn_restrictions',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('restriction_type', sa.String(64), nullable=False),
        sa.Column('from_segment_id', sa.String(64), sa.ForeignKey('road_segments.id'), nullable=False),
        sa.Column('to_segment_id', sa.String(64), sa.ForeignKey('road_segments.id'), nullable=False),
        sa.Column('junction_location', geoalchemy2.Geometry('POINT', srid=4326), nullable=False),
        sa.Column('start_time', sa.Time(), nullable=True),
        sa.Column('end_time', sa.Time(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
    )

    # 10. Temporary Restrictions
    op.create_table(
        'temporary_restrictions',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('restriction_type', sa.String(64), nullable=False),
        sa.Column('area_geometry', geoalchemy2.Geometry('GEOMETRY', srid=4326), nullable=False),
        sa.Column('start_timestamp', sa.DateTime(timezone=True), nullable=False),
        sa.Column('end_timestamp', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
    )

    # 11. Community Reports
    op.create_table(
        'community_reports',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('user_id', sa.String(64), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('report_type', sa.String(64), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.String(32), server_default='PENDING', nullable=False),
        sa.Column('confirmation_count', sa.Integer(), server_default='1', nullable=False),
        sa.Column('location', geoalchemy2.Geometry('POINT', srid=4326), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
    )

    # 12. Challan Events
    op.create_table(
        'challan_events',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('user_id', sa.String(64), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('violation_type', sa.String(64), nullable=False),
        sa.Column('fine_amount', sa.Float(), nullable=True),
        sa.Column('location', geoalchemy2.Geometry('POINT', srid=4326), nullable=True),
        sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
    )

    # 13. Offline Pack Versions
    op.create_table(
        'offline_pack_versions',
        sa.Column('id', sa.String(64), primary_key=True),
        sa.Column('region', sa.String(64), nullable=False),
        sa.Column('version', sa.String(64), nullable=False),
        sa.Column('file_size_bytes', sa.BigInteger(), nullable=False),
        sa.Column('checksum_sha256', sa.String(64), nullable=False),
        sa.Column('download_url', sa.String(512), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('offline_pack_versions')
    op.drop_table('challan_events')
    op.drop_table('community_reports')
    op.drop_table('temporary_restrictions')
    op.drop_table('turn_restrictions')
    op.drop_table('traffic_signal_junctions')
    op.drop_table('speed_limits')
    op.drop_table('road_segments')
    op.drop_table('enforcement_points')
    op.drop_table('data_sources')
    op.drop_table('user_preferences')
    op.drop_table('users')
