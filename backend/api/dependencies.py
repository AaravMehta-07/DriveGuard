import logging
from typing import AsyncGenerator
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import redis.asyncio as redis
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from redis.asyncio import Redis, ConnectionPool
import jwt
from jwt import PyJWKClient

from .config import settings

logger = logging.getLogger(__name__)

security = HTTPBearer(auto_error=False)

class User(BaseModel):
    id: str
    email: str | None = None
    role: str = "user"

# Database
engine = create_async_engine(settings.DATABASE_URL, echo=False, pool_size=10, max_overflow=20)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

# Redis
redis_pool = ConnectionPool.from_url(settings.REDIS_URL, decode_responses=True)

async def get_redis() -> AsyncGenerator[Redis, None]:
    client = Redis(connection_pool=redis_pool)
    try:
        yield client
    finally:
        await client.close()

# Auth
# Create a JWK client to fetch keys
jwks_client = PyJWKClient(str(settings.AUTH_JWKS_URL))

def validate_token(token: str) -> dict:
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        audience = settings.AUTH_ISSUER.split("/")[-1] if settings.AUTH_PROVIDER == "firebase" else None
        data = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            issuer=settings.AUTH_ISSUER,
            audience=audience,
        )
        return data
    except jwt.PyJWTError as e:
        logger.warning(f"Token validation failed: {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token")

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    payload = validate_token(credentials.credentials)
    user_id = payload.get("sub") or payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing subject")
        
    return User(
        id=user_id,
        email=payload.get("email"),
        role=payload.get("role", "user")
    )

async def get_optional_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User | None:
    if not credentials:
        return None
    try:
        payload = validate_token(credentials.credentials)
        user_id = payload.get("sub") or payload.get("user_id")
        if not user_id:
            return None
        return User(
            id=user_id,
            email=payload.get("email"),
            role=payload.get("role", "user")
        )
    except Exception:
        return None
