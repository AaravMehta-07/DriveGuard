import os

import pytest

try:
    import asyncpg
    HAS_ASYNCPG = True
except ImportError:
    HAS_ASYNCPG = False

import pytest_asyncio

# Use environment variable or default local test DB
DB_URL = os.environ.get("TEST_DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/driveguard_test")

@pytest_asyncio.fixture(scope="session")
async def db_pool():
    """Create a database connection pool for the test session."""
    if not HAS_ASYNCPG:
        pytest.skip("asyncpg is not installed in the local environment")

    try:
        pool = await asyncpg.create_pool(DB_URL, timeout=2.0)
        async with pool.acquire() as conn:
            await conn.execute("CREATE EXTENSION IF NOT EXISTS postgis;")
        yield pool
        await pool.close()
    except Exception as e:
        pytest.skip(f"PostgreSQL/PostGIS database not reachable: {e}")

@pytest_asyncio.fixture
async def db_conn(db_pool):
    """Provide a database connection with automatic cleanup for each test."""
    async with db_pool.acquire() as conn:
        tr = conn.transaction()
        await tr.start()
        try:
            yield conn
        finally:
            await tr.rollback()
