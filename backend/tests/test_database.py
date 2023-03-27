import os

import pytest

# for type hinting
from fastapi.testclient import TestClient

from backend.nba_backend.models.models import TranscriptTable
from tests.conftest import TestingSessionLocal, build_test_client
from tests.fixture.send_request import send_get_request, send_post_request

SAMPLE_DIR = "sample-data"
FILE_NAMES = ["sample3.mp3", "sample2.wav", "sample1.wav"]
FILE_PATHS = [os.path.join(SAMPLE_DIR, f_name) for f_name in FILE_NAMES]


@pytest.fixture
def client_fixture() -> TestClient:
    return build_test_client()


def test_datase_write(client_fixture: TestClient) -> None:
    response, _ = send_post_request(client_fixture, FILE_PATHS)
    temp_db = TestingSessionLocal()
    X = (
        temp_db.query(TranscriptTable)
        .order_by(TranscriptTable.transcript_id.desc())
        .first()
    )
    assert X is not None, "Transcript Record must exist"
    assert X.text == response.json()[-1]["text"]


def test_database_read(client_fixture: TestClient) -> None:
    current_id = 10240
    text = "Example Transcripted Text"
    temp_db = TestingSessionLocal()
    confidence_score = 0.95

    db_transcript = TranscriptTable(
        text=text, confidence_score=confidence_score, transcript_id=current_id
    )
    temp_db.add(db_transcript)
    temp_db.commit()

    response2 = send_get_request(client_fixture, current_id)
    print(response2.request.url)
    print(response2.json())
    assert text == response2.json()[-1]["text"], response2.json()
