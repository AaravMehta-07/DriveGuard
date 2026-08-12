import logging
import time

from fastapi import Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware

from backend.api.dependencies import get_redis_client

logger = logging.getLogger(__name__)

class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Redis-backed sliding window rate limiter middleware.
    Applies rate limits based on client IP.
    """
    def __init__(self, app, requests_per_minute: int = 120):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "127.0.0.1"
        key = f"rate_limit:{client_ip}:{int(time.time() // 60)}"

        try:
            redis_client = get_redis_client()
            current_count = await redis_client.incr(key)
            if current_count == 1:
                await redis_client.expire(key, 60)
            if current_count > self.requests_per_minute:
                await redis_client.close()
                return Response(
                    content='{"detail": "Rate limit exceeded. Try again in a minute."}',
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    media_type="application/json"
                )
            await redis_client.close()
        except Exception as e:
            logger.debug(f"Rate limiting check skipped due to Redis connection state: {e}")

        response = await call_next(request)
        return response
