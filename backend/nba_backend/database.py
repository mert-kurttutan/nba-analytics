from sqlmodel import create_engine

from nba_backend.config import settings

# if settings.DATABASE_URI is None:
#     raise OasstError("DATABASE_URI is not set", error_code=OasstErrorCode.DATABASE_URI_NOT_SET)

engine = create_engine(
    settings.DATABASE_URI,
    echo=settings.DEBUG_DATABASE_ECHO,
    isolation_level="REPEATABLE READ",
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
)
