import json
from datetime import datetime
from http import HTTPStatus
from math import ceil
from pathlib import Path
from typing import Optional

import alembic.command
import alembic.config
import fastapi
import redis.asyncio as redis
from fastapi_limiter import FastAPILimiter
from loguru import logger
from nba_backend.api.deps import api_auth, create_api_client
from nba_backend.api.v1.api import api_router
from nba_backend.config import settings
from nba_backend.database import engine
from nba_backend.exceptions import NBAError, NBAErrorCode
from nba_backend.schemas import protocol as protocol_schema
from nba_backend.utils.utils import utcnow
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel
from sqlmodel import Session
from starlette.middleware.cors import CORSMiddleware

# from worker.scheduled_tasks import create_task

app = fastapi.FastAPI() # title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")
startup_time: datetime = utcnow()


@app.exception_handler(NBAError)
async def nba_exception_handler(request: fastapi.Request, ex: NBAError):
    logger.error(f"{request.method} {request.url} failed: {repr(ex)}")

    return fastapi.responses.JSONResponse(
        status_code=int(ex.http_status_code),
        content=protocol_schema.NBAErrorResponse(
            message=ex.message,
            error_code=NBAErrorCode(ex.error_code),
        ).dict(),
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: fastapi.Request, ex: Exception):
    logger.exception(f"{request.method} {request.url} failed [UNHANDLED]: {repr(ex)}")
    status = HTTPStatus.INTERNAL_SERVER_ERROR
    return fastapi.responses.JSONResponse(
        status_code=status.value, content={"message": status.name, "error_code": NBAErrorCode.GENERIC_ERROR}
    )


# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

if settings.UPDATE_ALEMBIC:

    @app.on_event("startup")
    def alembic_upgrade():
        logger.info("Attempting to upgrade alembic on startup")
        try:
            alembic_ini_path = Path(__file__).parent / "alembic.ini"
            alembic_cfg = alembic.config.Config(str(alembic_ini_path))
            alembic_cfg.set_main_option("sqlalchemy.url", settings.DATABASE_URI)
            alembic.command.upgrade(alembic_cfg, "head")
            logger.info("Successfully upgraded alembic on startup")
        except Exception:
            logger.exception("Alembic upgrade failed on startup")


if settings.OFFICIAL_WEB_API_KEY:

    @app.on_event("startup")
    def create_official_web_api_client():
        with Session(engine) as session:
            try:
                api_auth(settings.OFFICIAL_WEB_API_KEY, db=session)
            except NBAError:
                logger.info("Creating official web API client")
                create_api_client(
                    session=session,
                    api_key=settings.OFFICIAL_WEB_API_KEY,
                    description="The official web client for the NBA backend.",
                    frontend_type="web",
                    trusted=True,
                )


if settings.ENABLE_PROM_METRICS:

    instrumentator = Instrumentator().instrument(app)

    @app.on_event("startup")
    async def enable_prom_metrics():
        instrumentator.expose(app)


if settings.RATE_LIMIT and False:

    @app.on_event("startup")
    async def connect_redis():
        async def http_callback(request: fastapi.Request, response: fastapi.Response, pexpire: int):
            """Error callback function when too many requests"""
            expire = ceil(pexpire / 1000)
            raise NBAError(
                f"Too Many Requests. Retry After {expire} seconds.",
                NBAErrorCode.TOO_MANY_REQUESTS,
                HTTPStatus.TOO_MANY_REQUESTS,
            )

        try:
            redis_client = redis.from_url(
                f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0", encoding="utf-8", decode_responses=True
            )
            logger.info(f"Connected to {redis_client=}")
            await FastAPILimiter.init(redis_client, http_callback=http_callback)
        except Exception:
            logger.exception("Failed to establish Redis connection")



app.include_router(api_router, prefix=settings.API_V1_STR)


def get_openapi_schema():
    return json.dumps(app.openapi())


def main():
    # Importing here so we don't import packages unnecessarily if we're
    # importing main as a module.
    import argparse

    import uvicorn

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--print-openapi-schema",
        default=False,
        help="Dumps the openapi schema to stdout",
        action="store_true",
    )
    parser.add_argument("--host", help="The host to run the server", default="0.0.0.0")
    parser.add_argument("--port", help="The port to run the server", default=8080)
    parser.add_argument(
        "--retry-scoring",
        default=False,
        help="Retry scoring failed message trees",
        action="store_true",
    )

    args = parser.parse_args()

    if args.print_openapi_schema:
        print(get_openapi_schema())


    if not (args.print_openapi_schema or args.retry_scoring):
        print("started")
        uvicorn.run(app, host=args.host, port=args.port)
        print("finished")
    print("finished")


if __name__ == "__main__":
    main()