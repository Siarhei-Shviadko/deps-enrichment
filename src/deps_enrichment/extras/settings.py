from typing import Optional

from pydantic import BaseSettings

from .datasource import DBDialect, DBDriver

__all__ = ["SSLSettings", "DatabaseSettings", "ServiceInfoSettings", "SentrySettings"]


class SSLSettings(BaseSettings):
    key: str = ""
    cert: str = ""
    rootcert: str = ""
    mode: str = "verify-full"

    class Config:
        env_prefix = "DATABASE_SSL"


class DatabaseSettings(BaseSettings):
    user: str
    password: str
    host: str
    port: str
    db: str
    ssl: SSLSettings = SSLSettings()
    dialect: DBDialect = DBDialect.POSTGRES
    driver: DBDriver = DBDriver.PSYCOPG2
    require_secure_transport: bool = False

    class Config:
        env_prefix = "DATABASE_"


class ServiceInfoSettings(BaseSettings):
    tag: str = ""
    date: str = ""
    hash: str = ""

    class Config:
        env_prefix = "SERVICE_INFO_"


class SentrySettings(BaseSettings):
    enabled: bool = False
    trace_enabled: bool = False
    dsn: Optional[str] = None
    traces_sample_rate: Optional[float] = 0

    class Config:
        env_prefix = "SENTRY_"
        allow_mutation = False
