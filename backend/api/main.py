import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .middleware.logging_middleware import LoggingMiddleware
from .middleware.rate_limit import RateLimitMiddleware
from .middleware.request_id import RequestIdMiddleware
from .routers import admin, auth, challan, community, compliance, enforcement, health, offline, trips, users

logger = logging.getLogger(__name__)

# Validate CORS in production environment
if getattr(settings, "ENV", "dev") == "production" and "*" in settings.CORS_ORIGINS:
    raise RuntimeError("Wildcard CORS origins ['*'] are strictly prohibited in production configuration.")

app = FastAPI(
    title="DriveGuard API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)
app.add_middleware(LoggingMiddleware)
app.add_middleware(RequestIdMiddleware)
app.add_middleware(RateLimitMiddleware, requests_per_minute=120)

api_prefix = "/api/v1"

app.include_router(health.router, prefix=api_prefix)
app.include_router(auth.router, prefix=api_prefix)
app.include_router(enforcement.router, prefix=api_prefix)
app.include_router(compliance.router, prefix=api_prefix)
app.include_router(community.router, prefix=api_prefix)
app.include_router(trips.router, prefix=api_prefix)
app.include_router(offline.router, prefix=api_prefix)
app.include_router(admin.router, prefix=api_prefix)
app.include_router(users.router, prefix=api_prefix)
app.include_router(challan.router, prefix=api_prefix)
