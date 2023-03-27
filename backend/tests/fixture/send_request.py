import json
import os
from pathlib import Path

# One standard way to produce testclient in fastapi
from fastapi.testclient import TestClient
from httpx._models import Response

from nba_backend import PathParams, TranscriptConfig

API_KEY = os.environ["API_KEY"]
API_REGION = os.environ["API_REGION"]
RESPONSE_DIR = "response-data"


def send_post_request(
    client: TestClient,
    file_paths: list[str],
    is_async: bool = False,
    is_continuous: bool = True,
    is_detailed: bool = True,
    is_process: bool = True,
    is_batched: bool = False,
) -> tuple[Response, TranscriptConfig]:
    transcript_config = TranscriptConfig(
        file_name="",
        is_continuous=is_continuous,
        is_async=is_async,
        is_detailed=is_detailed,
        is_process=is_process,
        is_batched=is_batched,
        API_KEY=API_KEY,
        API_REGION=API_REGION,
    )
    post_payload = transcript_config.json()

    result_files = [
        ("received_files", (Path(f_path).name, open(f_path, "rb")))
        for f_path in file_paths
    ]

    r = client.post(
        f"/{PathParams.TRANSCRIBE}",
        files=result_files,
        data={"transcript": json.dumps(post_payload)},
    )

    file_arr_id = "-".join(Path(f_path).name for f_path in file_paths)
    Path(f"{RESPONSE_DIR}/{file_arr_id}").mkdir(parents=True, exist_ok=True)
    response_path = os.path.join(
        RESPONSE_DIR, file_arr_id, transcript_config.get_name()
    )
    with open(response_path, "w", encoding="utf-8") as outfile:
        json.dump(json.loads(r.text), outfile)

    return r, transcript_config


def send_get_request(client: TestClient, transcript_id: list[int] | int) -> Response:
    if isinstance(transcript_id, int):
        transcript_id = [transcript_id]

    query_params = {"transcript_id": transcript_id}

    r = client.get(
        f"/{PathParams.READ}/",
        params=query_params,
    )

    return r
