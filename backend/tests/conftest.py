import sys
from typing import Generator
from unittest import mock

import pytest

# One standard way to produce testclient in fastapi
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from backend.nba_backend.database import Base
from nba_backend import app
from nba_backend.api import get_db
from tests.fixture.mock_response import mocked_requests_get

SQLALCHEMY_DATABASE_URL = "sqlite:///db-store/test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(bind=engine)


def override_get_db() -> Generator[Session, None, None]:
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


def build_test_client() -> TestClient:
    # Initialize client insiide test function after patch mocking,
    # otherwise mock.patching would not work since fastapi
    # stores reference to original app modules and keep
    # using original methods even after mock.patching

    # test app for fastapi
    client = TestClient(app)
    app.dependency_overrides[get_db] = override_get_db

    return client


def pytest_addoption(parser: pytest.Parser) -> None:
    """This allows us to check for these params in sys.argv."""
    parser.addoption("--mock-network", action="store_true", default=False)
    parser.addoption("--no-output", action="store_true", default=False)


@pytest.fixture(scope="session", autouse=True)
def default_session_fixture(request: pytest.FixtureRequest) -> None:
    """
    :type request: _pytest.python.SubRequest
    :return:
    """
    if "--mock-network" not in sys.argv:
        return
    mocked_function_arr = [
        "app.transcriber.transcription.speech_recognize_continuous_from_file",
        "app.transcriber.transcription.speech_recognize_once_from_file",
    ]
    patched_arr = [
        mock.patch(mocked, side_effect=mocked_requests_get)
        for mocked in mocked_function_arr
    ]

    for patched in patched_arr:
        patched.start()

    def unpatch() -> None:
        for patched in patched_arr:
            patched.stop()

    request.addfinalizer(unpatch)


@pytest.fixture(autouse=True)
def test_db() -> Generator[None, None, None]:
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
