import os
from typing import Any, Dict, List, Optional

from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator

my_var = os.environ.get("SQL_URL")

if my_var:
    config.set_main_option()


class Settings(BaseSettings):
    PROJECT_NAME: str = "open-assistant backend"
    API_V1_STR: str = "/api/v1"
    OFFICIAL_WEB_API_KEY: str = "1234"

    # Encryption fields for handling the web generated JSON Web Tokens.
    # These fields need to be shared with the web's auth settings in order to
    # correctly decrypt the web tokens.
    AUTH_INFO: bytes = b"NextAuth.js Generated Encryption Key"
    AUTH_SALT: bytes = b""
    AUTH_LENGTH: int = 32
    AUTH_SECRET: bytes = b"O/M2uIbGj+lDD2oyNa8ax4jEOJqCPJzO53UbWShmq98="
    AUTH_COOKIE_NAME: str = "next-auth.session-token"
    AUTH_ALGORITHM: str = "HS256"
    AUTH_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    AUTH_DISCORD_CLIENT_ID: str = ""
    AUTH_DISCORD_CLIENT_SECRET: str = ""

    POSTGRES_HOST: str = os.environ.get("POSTGRES_HOST", None)
    POSTGRES_PORT: str = os.environ.get("POSTGRES_PORT", None)
    POSTGRES_USER: str = os.environ.get("POSTGRES_USER", None)
    POSTGRES_PASSWORD: str = os.environ.get("POSTGRES_PASSWORD", None)
    POSTGRES_DB: str = os.environ.get("POSTGRES_DB", None)
    DATABASE_URI: Optional[PostgresDsn] = None
    DATABASE_MAX_TX_RETRY_COUNT: int = 3

    DATABASE_POOL_SIZE = 75
    DATABASE_MAX_OVERFLOW = 20

    RATE_LIMIT: bool = True
    MESSAGE_SIZE_LIMIT: int = 2000
    REDIS_HOST: str = "localhost"
    REDIS_PORT: str = "6379"

    DEBUG_USE_SEED_DATA: bool = False
    DEBUG_ALLOW_SELF_LABELING: bool = False  # allow users to label their own messages
    DEBUG_ALLOW_SELF_RANKING: bool = False  # allow users to rank their own messages
    DEBUG_ALLOW_DUPLICATE_TASKS: bool = (
        False  # offer users tasks to which they already responded
    )
    DEBUG_SKIP_EMBEDDING_COMPUTATION: bool = False
    DEBUG_SKIP_TOXICITY_CALCULATION: bool = False
    DEBUG_DATABASE_ECHO: bool = False
    DEBUG_IGNORE_TOS_ACCEPTANCE: bool = (  # ignore whether users accepted the ToS
        True  # TODO: set False after ToS acceptance UI was added to web-frontend
    )

    DUPLICATE_MESSAGE_FILTER_WINDOW_MINUTES: int = 120

    HUGGING_FACE_API_KEY: str = ""

    ROOT_TOKENS: List[str] = [
        "1234"
    ]  # supply a string that can be parsed to a json list

    ENABLE_PROM_METRICS: bool = True  # enable prometheus metrics at /metrics

    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            print(f"here {v}")
            return v
        x = PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            port=values.get("POSTGRES_PORT"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )
        print(f"here {x}")
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            port=values.get("POSTGRES_PORT"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    BACKEND_CORS_ORIGINS_CSV: Optional[
        str
    ]  # allow setting CORS origins as comma separated values
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(
        cls, v: Optional[List[str]], values: Dict[str, Any]
    ) -> List[str]:
        s = values.get("BACKEND_CORS_ORIGINS_CSV")
        if isinstance(s, str):
            v = [i.strip() for i in s.split(",")]
            return v
        return v

    UPDATE_ALEMBIC: bool = True

    USER_STATS_INTERVAL_DAY: int = 5  # minutes
    USER_STATS_INTERVAL_WEEK: int = 15  # minutes
    USER_STATS_INTERVAL_MONTH: int = 60  # minutes
    USER_STATS_INTERVAL_TOTAL: int = 240  # minutes
    USER_STREAK_UPDATE_INTERVAL: int = 4  # Hours

    @validator(
        "USER_STATS_INTERVAL_DAY",
        "USER_STATS_INTERVAL_WEEK",
        "USER_STATS_INTERVAL_MONTH",
        "USER_STATS_INTERVAL_TOTAL",
        "USER_STREAK_UPDATE_INTERVAL",
    )
    def validate_user_stats_intervals(cls, v: int):
        if v < 1:
            raise ValueError(v)
        return v

    CACHED_STATS_UPDATE_INTERVAL: int = 60  # minutes

    RATE_LIMIT_TASK_USER_TIMES: int = 30
    RATE_LIMIT_TASK_USER_MINUTES: int = 4
    RATE_LIMIT_TASK_API_TIMES: int = 10_000
    RATE_LIMIT_TASK_API_MINUTES: int = 1

    RATE_LIMIT_ASSISTANT_USER_TIMES: int = 4
    RATE_LIMIT_ASSISTANT_USER_MINUTES: int = 2

    RATE_LIMIT_PROMPTER_USER_TIMES: int = 8
    RATE_LIMIT_PROMPTER_USER_MINUTES: int = 2

    TASK_VALIDITY_MINUTES: int = 60 * 24 * 2  # tasks expire after 2 days

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        env_nested_delimiter = "__"


settings = Settings()
