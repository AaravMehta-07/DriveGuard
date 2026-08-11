import pytest
import asyncpg
import pytest_asyncio
import os

# Use environment variable or default local test DB
DB_URL = os.environ.get("TEST_DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/driveguard_test")

@pytest_asyncio.fixture(scope="session")
async def db_pool():
    """Create a database connection pool for the test session."""
    pool = await asyncpg.create_pool(DB_URL)
    
    # Ensure PostGIS is enabled
    async with pool.acquire() as conn:
        await conn.execute("CREATE EXTENSION IF NOT EXISTS postgis;")
        
        # Verify PostGIS is working
        val = await conn.fetchval("SELECT postgis_version();")
        assert val is not None, "PostGIS extension not available"
    
    yield pool
    await pool.close()

@pytest_asyncio.fixture
async def db_conn(db_pool):
    """Provide a database connection with automatic cleanup for each test."""
    async with db_pool.acquire() as conn:
        tr = conn.transaction()
        await tr.start()
        
        try:
            yield conn
        finally:
            # Always rollback after test to ensure cleanup
            await tr.rollback()
