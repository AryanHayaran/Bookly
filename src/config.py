from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    # Database full URL (used by SQLAlchemy or async engine)
    DATABASE_URL: str

    # JWT settings
    JWT_SECRET: str
    JWT_ALGORITHM: str

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Email (FastAPI-Mail)
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_FROM_NAME: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True

    # App domain or frontend domain
    DOMAIN: str

    # Optional breakdown for building DATABASE_URL dynamically
    DB_HOST: Optional[str] = None
    DB_NAME: Optional[str] = None
    DB_USER: Optional[str] = None
    DB_PASSWORD: Optional[str] = None
    DB_PORT: Optional[str] = "5432"  # default for PostgreSQL

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


Config = Settings()

# Celery settings (or redis job queues)
broker_url = Config.REDIS_URL
result_backend = Config.REDIS_URL