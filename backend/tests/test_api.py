"""Dummy test script. If necessary, I can add
to make it a PROPER testing process.
"""

import json
import os
from itertools import product
from typing import Any

import pytest

# for type hinting
from fastapi.testclient import TestClient

from nba_backend import DataDirs, TranscriptConfig
from tests.conftest import build_test_client
from tests.fixture.send_request import send_post_request

# TODO: cover more different types of audio files
# this should be rather easy, just add kind of audio you want to
# test to sample-data and then collect raw data to collect response from
# azure api, then test with mock-network


SAMPLE_DIR = "sample-data"
FILE_NAMES = ["sample3.mp3", "sample2.wav", "sample1.wav"]
FILE_PATHS = [os.path.join(SAMPLE_DIR, f_name) for f_name in FILE_NAMES]


@pytest.fixture
def client_fixture() -> TestClient:
    return build_test_client()


def test_transcription_response(client_fixture: TestClient) -> None:
    """Check for successful response"""
    response, _ = send_post_request(client_fixture, FILE_PATHS)
    assert (
        response.status_code == 200
    ), "Wrong status code, It must be a successful response"


def test_json_processing(client_fixture: TestClient) -> None:
    """Test format after processing"""
    somelists = [
        [True, False],
        [True, False],
        [True, False],
        [True, False],
    ]

    for is_async, is_continuous, is_detailed, is_process in product(*somelists):
        response, transcript_config = send_post_request(
            client_fixture, FILE_PATHS, is_async, is_continuous, is_detailed, is_process
        )
        result_json = json.loads(response.text)
        check_processed_format(result_json, FILE_PATHS, transcript_config)


def test_transcript_file(client_fixture: TestClient) -> None:
    """Test for removing file"""
    send_post_request(client_fixture, FILE_PATHS)
    assert not os.path.exists(DataDirs.TEMP_DIR)


def test_long_transcript(client_fixture: TestClient) -> None:
    """Test for very long audio file"""
    assert True


def check_processed_format(
    result_arr: list[Any], file_paths: list[str], transcript_config: TranscriptConfig
) -> None:
    result_keys = {
        "text",
        "confidence_score",
        "recognition_status",
        "reason_message",
        "reason_code",
    }

    assert len(result_arr) == len(file_paths), "file names num must match result num"

    if not transcript_config.is_process:
        return
    for result in result_arr:
        assert (
            set(result.keys()) == result_keys
        ), f"Key of result json must be {result_keys}"

        assert isinstance(
            result["confidence_score"], float
        ), "wrong type for confidence score"
        assert all(
            isinstance(status, str) for status in result["recognition_status"]
        ), "wrong type for recognition status"
        assert isinstance(result["text"], str), "wrong type for output text"

        # ensure non empty result
        assert (
            result["text"]
            and result["recognition_status"]
            and result["confidence_score"]
            or not transcript_config.is_detailed
        ), "Transcripted output must be non-empty"
