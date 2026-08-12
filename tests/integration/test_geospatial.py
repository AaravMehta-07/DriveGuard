"""
PostGIS Geography Correctness Regression Tests

These tests explicitly prove:
- 100m buffer means approximately 100 meters
- Distance calculations are in meters, not degrees  
- Route-corridor width is metric
- Mumbai route measurements are correct
- Latitude does not incorrectly affect distance
"""

import math

import pytest

pytestmark = pytest.mark.asyncio

async def test_buffer_is_metric(db_conn):
    """1. Create a point at Mumbai coordinates, buffer by 100m using geography cast, verify resulting polygon spans ~100m."""
    # Point at Mumbai: 19.076°N, 72.877°E
    query = """
    SELECT 
        ST_Area(ST_Buffer(ST_MakePoint(72.877, 19.076)::geography, 100)) as area_sqm;
    """
    row = await db_conn.fetchrow(query)
    area = row['area_sqm']
    # A circle of radius 100m should have an area of approx pi * 100^2 = 31415 sqm.
    expected_area = math.pi * 100 * 100
    assert abs(area - expected_area) / expected_area < 0.05, f"Area {area} is not within 5% of {expected_area} sqm"

async def test_distance_is_meters(db_conn):
    """2. Two points 1km apart in Mumbai, verify ST_Distance with geography returns ~1000m."""
    # 0.009 degrees latitude is roughly 1km
    query = """
    SELECT ST_Distance(
        ST_MakePoint(72.877, 19.076)::geography,
        ST_MakePoint(72.877, 19.085)::geography
    ) as dist;
    """
    row = await db_conn.fetchrow(query)
    dist = row['dist']
    # roughly 1000m (1 degree lat = 111.32km, 0.009 * 111320 = 1001.88m)
    expected_dist = 1001.88
    assert abs(dist - expected_dist) / expected_dist < 0.05, f"Distance {dist} is not within 5% of {expected_dist} m"

async def test_buffer_at_different_latitudes(db_conn):
    """3. Same buffer at equator and at Mumbai latitude should produce same metric result."""
    query = """
    SELECT 
        ST_Area(ST_Buffer(ST_MakePoint(0, 0)::geography, 100)) as area_equator,
        ST_Area(ST_Buffer(ST_MakePoint(72.877, 19.076)::geography, 100)) as area_mumbai;
    """
    row = await db_conn.fetchrow(query)
    assert abs(row['area_equator'] - row['area_mumbai']) / row['area_equator'] < 0.05, "Areas differ significantly between latitudes"

async def test_route_corridor_width(db_conn):
    """4. Create a LineString route in Mumbai, buffer by 50m, verify a point 40m perpendicular is inside, point 60m away is outside."""
    query = """
    WITH route AS (
        SELECT ST_MakeLine(ST_MakePoint(72.877, 19.076), ST_MakePoint(72.877, 19.085))::geography as geom
    ),
    corridor AS (
        SELECT ST_Buffer(geom, 50) as poly FROM route
    )
    SELECT 
        -- Approx 40m East (1 deg long at 19N is approx 105km, so 40m is ~0.00038 deg)
        ST_Intersects((SELECT poly FROM corridor), ST_MakePoint(72.87738, 19.080)::geography) as inside_40m,
        -- Approx 60m East (~0.00057 deg)
        ST_Intersects((SELECT poly FROM corridor), ST_MakePoint(72.87757, 19.080)::geography) as outside_60m;
    """
    row = await db_conn.fetchrow(query)
    assert row['inside_40m'] is True, "40m point should be inside 50m corridor"
    assert row['outside_60m'] is False, "60m point should be outside 50m corridor"

async def test_along_route_distance(db_conn):
    """5. Create a route with known geometry, place a point at known position, verify ST_LineLocatePoint + ST_Length gives correct meters."""
    query = """
    WITH route AS (
        SELECT ST_MakeLine(ST_MakePoint(72.877, 19.076), ST_MakePoint(72.877, 19.085))::geography as geom
    ),
    pt AS (
        SELECT ST_MakePoint(72.877, 19.0805)::geography as geom -- exactly halfway
    )
    SELECT 
        (ST_LineLocatePoint((SELECT geom::geometry FROM route), (SELECT geom::geometry FROM pt)) * ST_Length((SELECT geom FROM route))) as dist_along,
        ST_Length((SELECT geom FROM route)) / 2 as expected_dist;
    """
    row = await db_conn.fetchrow(query)
    assert abs(row['dist_along'] - row['expected_dist']) / row['expected_dist'] < 0.05, "Distance along route is not metric"

async def test_multilinestring_route(db_conn):
    """6. Verify along-route calculations work with MultiLineString routes."""
    query = """
    WITH route AS (
        SELECT ST_Multi(ST_MakeLine(ST_MakePoint(72.877, 19.076), ST_MakePoint(72.877, 19.085)))::geography as geom
    )
    SELECT ST_Length(geom) as total_len FROM route;
    """
    row = await db_conn.fetchrow(query)
    expected_dist = 1001.88
    assert abs(row['total_len'] - expected_dist) / expected_dist < 0.05

async def test_enforcement_in_corridor_uses_meters(db_conn):
    """7. Insert enforcement points at known positions, query with 50m corridor, verify only points within 50m are returned."""
    await db_conn.execute("""
        CREATE TEMP TABLE test_cameras (id serial, geom geography);
        INSERT INTO test_cameras (geom) VALUES 
            (ST_MakePoint(72.87738, 19.080)::geography), -- ~40m away
            (ST_MakePoint(72.87757, 19.080)::geography); -- ~60m away
    """)
    query = """
    WITH route_corridor AS (
        SELECT ST_Buffer(ST_MakeLine(ST_MakePoint(72.877, 19.076), ST_MakePoint(72.877, 19.085))::geography, 50) as poly
    )
    SELECT count(*) as cnt FROM test_cameras, route_corridor WHERE ST_Intersects(test_cameras.geom, route_corridor.poly);
    """
    row = await db_conn.fetchrow(query)
    assert row['cnt'] == 1, "Only the 40m point should intersect the 50m corridor"

async def test_direction_filtering(db_conn):
    """8. Insert cameras with known directions, query with heading, verify direction filtering works."""
    await db_conn.execute("""
        CREATE TEMP TABLE test_cameras_dir (id serial, geom geography, heading int, heading_tolerance int);
        INSERT INTO test_cameras_dir (geom, heading, heading_tolerance) VALUES 
            (ST_MakePoint(72.877, 19.080)::geography, 0, 45),    -- North facing
            (ST_MakePoint(72.877, 19.081)::geography, 180, 45);  -- South facing
    """)
    # Travel direction is North (0 degrees)
    query = """
    SELECT count(*) as cnt FROM test_cameras_dir 
    WHERE abs((heading - 0 + 540) % 360 - 180) <= heading_tolerance;
    """
    row = await db_conn.fetchrow(query)
    assert row['cnt'] == 1, "Only the north facing camera should match a north travel direction"

async def test_road_level_filtering(db_conn):
    """9. Insert cameras at road_level=0 and road_level=1, query with road_level=0, verify flyover camera excluded."""
    await db_conn.execute("""
        CREATE TEMP TABLE test_cameras_lvl (id serial, geom geography, road_level int);
        INSERT INTO test_cameras_lvl (geom, road_level) VALUES 
            (ST_MakePoint(72.877, 19.080)::geography, 0),
            (ST_MakePoint(72.877, 19.080)::geography, 1);
    """)
    query = """
    SELECT count(*) as cnt FROM test_cameras_lvl WHERE road_level = 0;
    """
    row = await db_conn.fetchrow(query)
    assert row['cnt'] == 1, "Flyover camera should be excluded"

async def test_camera_ahead_on_route(db_conn):
    """10. Insert camera at known along-route distance, verify returned distance matches expected meters."""
    query = """
    WITH route AS (
        SELECT ST_MakeLine(ST_MakePoint(72.877, 19.076), ST_MakePoint(72.877, 19.085))::geography as geom
    ),
    cam AS (
        SELECT ST_MakePoint(72.877, 19.0805)::geography as geom
    )
    SELECT ST_Distance(
        (SELECT ST_StartPoint(geom::geometry)::geography FROM route),
        (SELECT geom FROM cam)
    ) as dist_meters;
    """
    row = await db_conn.fetchrow(query)
    dist = row['dist_meters']
    expected_dist = 500.94 # half of 1001.88
    assert abs(dist - expected_dist) / expected_dist < 0.05, "Camera distance ahead should match metric expectation"

async def test_opposite_direction_camera_excluded(db_conn):
    """11. Insert camera monitoring opposite direction, verify it's excluded from direction-filtered results."""
    await db_conn.execute("""
        CREATE TEMP TABLE test_cameras_opp (id serial, geom geography, heading int, heading_tolerance int);
        INSERT INTO test_cameras_opp (geom, heading, heading_tolerance) VALUES 
            (ST_MakePoint(72.877, 19.080)::geography, 180, 45);  -- South facing
    """)
    # Travel direction is North (0 degrees)
    query = """
    SELECT count(*) as cnt FROM test_cameras_opp 
    WHERE abs((heading - 0 + 540) % 360 - 180) <= heading_tolerance;
    """
    row = await db_conn.fetchrow(query)
    assert row['cnt'] == 0, "Opposite direction camera should be excluded"
