from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost:5432/driveguard"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    S3_ENDPOINT: Optional[str] = None
    S3_ACCESS_KEY: Optional[str] = None
    S3_SECRET_KEY: Optional[str] = None
    S3_BUCKET: Optional[str] = None
    
    AUTH_PROVIDER: str = "firebase"
    AUTH_JWKS_URL: AnyHttpUrl = "https://www.googleapis.com/service_accounts/v1/jwk/securetoken@system.gserviceaccount.com"
    AUTH_ISSUER: str = "https://securetoken.google.com/driveguard"
    
    SENTRY_DSN: Optional[str] = None
    POSTHOG_KEY: Optional[str] = None
    LLM_PROVIDER: Optional[str] = None
    LLM_API_KEY: Optional[str] = None
    
    CORS_ORIGINS: List[str] = ["*"]
    API_RATE_LIMIT: str = "100/minute"
    
    ENV: str = "dev"
    LOG_LEVEL: str = "INFO"
    
    COMPLIANCE_POLICY_VERSION: str = "1.0"
    ALERT_POLICY_VERSION: str = "1.0"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
