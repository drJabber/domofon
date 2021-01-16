import logging
import sys
from typing import List, cast

from databases import DatabaseURL
from loguru import logger
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

from app.core.logging import InterceptHandler

API_PREFIX_V1 = "/api/v1"

JWT_TOKEN_PREFIX = "Token"  # noqa: S105
VERSION = "0.1.0"

config = Config(".env")

DEBUG: bool = config("DEBUG", cast=bool, default=False)

DATABASE_URL: DatabaseURL = config("DB_CONNECTION", cast=DatabaseURL)
MAX_CONNECTIONS_COUNT: int = config("MAX_CONNECTIONS_COUNT", cast=int, default=10)
MIN_CONNECTIONS_COUNT: int = config("MIN_CONNECTIONS_COUNT", cast=int, default=10)

SECRET_KEY: Secret = config("SECRET_KEY", cast=Secret)

PROJECT_NAME: str = config("PROJECT_NAME", default="Domofon")
ALLOWED_HOSTS: List[str] = config(
    "ALLOWED_HOSTS",
    cast=CommaSeparatedStrings,
    default="",
)

# restrict some paths for some hosts
ALLOWED_HOSTS_FOR_PATHS = {}
RESTRICTED_PATH_1: str = config("RESTRICTED_PATH_1", cast=CommaSeparatedStrings, default="")
for index in range(100):
    restricted_path = API_PREFIX_V1+config(f"RESTRICTED_PATH_{index}", cast=str, default="")
    allowed_hosts_for_path = config(f"ALLOWED_HOSTS_FOR_PATH_{index}", cast=CommaSeparatedStrings, default="")
    if restricted_path:
        ALLOWED_HOSTS_FOR_PATHS[restricted_path] = allowed_hosts_for_path

#JWT
JWT_SUBJECT: str = config("JWT_SUBJECT", cast=str, default="access")
JWT_ALGORITHM: str = config("JWT_ALGORITHM", cast=str, default="HS256")

#OAuth2 configuration
ACCESS_TOKEN_EXPIRE_MINUTES: int = config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int, default=60 * 24 * 7)
REFRESH_TOKEN_EXPIRE_MINUTES: int = config("REFRESH_TOKEN_EXPIRE_MINUTES", cast=int, default=60 * 24 * 30)

# openapi config
OPENAPI_JSON_URL: str = config("OPENAPI_JSON_URL", cast=str, default="/openapi.json")
OPENAPI_DOCS_PATH: str = config("OPENAPI_DOCS_PATH", cast=str, default="/docs")
OPENAPI_REDOC_PATH: str = config("OPENAPI_REDOC_PATH", cast=str, default="/redoc")


# logging configuration

LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
LOGGERS = ("uvicorn.asgi", "uvicorn.access")

logging.getLogger().handlers = [InterceptHandler()]
for logger_name in LOGGERS:
    logging_logger = logging.getLogger(logger_name)
    logging_logger.handlers = [InterceptHandler(level=LOGGING_LEVEL)]

logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])

#ufanet

UFANET_SERVICE_URL: str = config("UFANET_SERVICE_URL", cast=str, default="https://dom.ufanet.ru")
UFANET_LOGIN_API: str = config("UFANET_LOGIN_API", cast=str, default="/api/v1/auth/auth_by_contract/")
UFANET_REFRESH_TOKEN_API: str = config("UFANET_REFRESH_TOKEN_API", cast=str, default="/api/v1/auth/refresh/")
UFANET_SKUD_API: str = config("UFANET_SKUD_API", cast=str, default="/api/v0/skud/shared/")
