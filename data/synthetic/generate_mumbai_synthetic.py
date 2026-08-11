import json
import random
import uuid
import argparse
import logging
from datetime import datetime, timezone
import uuid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mumbai bounding box
LAT_MIN, LAT_MAX = 18.9, 19.3
LON_MIN, LON_MAX = 72.7, 73.0

ROADS = [
    "Western Express Highway",
    "Eastern Express Highway",
    "Marine Drive",
    "SV Road",
    "LBS Marg",
    "Bandra Kurla Complex Road",
    "Jogeshwari Vikhroli Link Road"
]

def generate_uuid() -> str:
    return str(uuid.uuid4())

def get_random_mumbai_point():
    lat = random.uniform(LAT_MIN, LAT_MAX)
    lon = random.uniform(LON_MIN, LON_MAX)
    return f"POINT({lon} {lat})"

def get_random_mumbai_linestring():
    lon1 = random.uniform(LON_MIN, LON_MAX)
    lat1 = random.uniform(LAT_MIN, LAT_MAX)
    lon2 = lon1 + random.uniform(-0.01, 0.01)
    lat2 = lat1 + random.uniform(-0.01, 0.01)
    return f"LINESTRING({lon1} {lat1}, {lon2} {lat2})"

def generate_enforcement_points(count=50):
    points = []
    types = ["speed_camera", "red_light_camera", "no_parking_zone"]
    for _ in range(count):
        points.append({
            "id": generate_uuid(),
            "geom": get_random_mumbai_point(),
            "point_type": random.choice(types),
            "road_level": random.choice([0, 1]),
            "structure_type": random.choice(["surface", "elevated"]),
            "synthetic": True,
            "created_at": datetime.now(timezone.utc).isoformat()
        })
    return points

def generate_road_segments(count=100):
    segments = []
    types = ["motorway", "primary", "secondary", "residential"]
    for _ in range(count):
        segments.append({
            "id": generate_uuid(),
            "geom": get_random_mumbai_linestring(),
            "name": random.choice(ROADS),
            "highway_type": random.choice(types),
            "synthetic": True,
            "created_at": datetime.now(timezone.utc).isoformat()
        })
    return segments

def main():
    parser = argparse.ArgumentParser(description="Generate synthetic Mumbai data.")
    parser.add_argument("--out-json", type=str, default="mumbai_synthetic_fixture.json")
    parser.add_argument("--out-sql", type=str, default="mumbai_synthetic_fixture.sql")
    args = parser.parse_args()

    data = {
        "enforcement_points": generate_enforcement_points(50),
        "road_segments": generate_road_segments(100)
    }

    with open(args.out_json, "w") as f:
        json.dump(data, f, indent=2)
    logger.info(f"Generated JSON output: {args.out_json}")

    with open(args.out_sql, "w") as f:
        f.write("-- Synthetic Test Data for Mumbai\n")
        f.write("-- GENERATED FILE: ALL SYNTHETIC=TRUE\n\n")
        
        for p in data["enforcement_points"]:
            stmt = f"INSERT INTO enforcement_points (id, geom, point_type, road_level, structure_type, synthetic) VALUES ('{p['id']}', ST_GeomFromText('{p['geom']}', 4326), '{p['point_type']}', {p['road_level']}, '{p['structure_type']}', true);\n"
            f.write(stmt)
            
        for s in data["road_segments"]:
            stmt = f"INSERT INTO road_segments (id, geom, name, highway_type, synthetic) VALUES ('{s['id']}', ST_GeomFromText('{s['geom']}', 4326), '{s['name']}', '{s['highway_type']}', true);\n"
            f.write(stmt)
            
    logger.info(f"Generated SQL output: {args.out_sql}")

if __name__ == "__main__":
    main()
