import asyncio
import logging
import argparse
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

# Import models and registries
from backend.models.base import Base
from backend.models.users import User
from backend.models.sources import DataSource
from backend.ingestion.sources.source_registry import SourceRegistry

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

async def seed_sources(session: AsyncSession):
    registry = SourceRegistry(session)
    await registry.initialize_sources()
    logger.info("Data sources seeded successfully.")

async def seed_admin_user(session: AsyncSession):
    from sqlalchemy import select
    stmt = select(User).where(User.username == "admin")
    result = await session.execute(stmt)
    admin = result.scalar_one_or_none()
    
    if not admin:
        admin_user = User(
            username="admin",
            email="admin@driveguard.in",
            hashed_password=get_password_hash("admin"), # Default password, should be changed
            synthetic=False
        )
        session.add(admin_user)
        await session.commit()
        logger.info("Admin user created successfully.")
    else:
        logger.info("Admin user already exists.")

async def main():
    parser = argparse.ArgumentParser(description="Seed the DriveGuard database.")
    parser.add_argument("--db-url", type=str, default="postgresql+asyncpg://postgres:postgres@localhost:5432/driveguard", help="Database connection URL")
    args = parser.parse_args()

    engine = create_async_engine(args.db_url, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        await seed_sources(session)
        await seed_admin_user(session)

    await engine.dispose()
    logger.info("Database seeding completed.")

if __name__ == "__main__":
    asyncio.run(main())
