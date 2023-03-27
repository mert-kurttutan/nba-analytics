"""Utils"""
import os
import shutil
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from functools import wraps
from typing import Any

from loguru import logger


def utcnow() -> datetime:
    """Return the current utc date and time with tzinfo set to UTC."""
    return datetime.now(timezone.utc)


def unaware_to_utc(d: datetime | None) -> datetime:
    """Set timezeno to UTC if datetime is unaware (tzinfo == None)."""
    if d and d.tzinfo is None:
        return d.replace(tzinfo=timezone.utc)
    return d


class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""


class ScopeTimer:
    def __init__(self):
        self.start()

    def start(self) -> None:
        """Measure new start time"""
        self.start_time = time.perf_counter()

    def stop(self) -> float:
        """Store and return the elapsed time"""
        self.elapsed = time.perf_counter() - self.start_time
        return self.elapsed

    def __enter__(self):
        """Start a new timer as a context manager"""
        self.start()
        return self

    def __exit__(self, *exc_info):
        """Stop the context manager timer"""
        self.stop()


def log_timing(
    func=None, *, log_kwargs: bool = False, level: int | str = "DEBUG"
) -> None:
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            timer = ScopeTimer()
            result = func(*args, **kwargs)
            elapsed = timer.stop()
            if log_kwargs:
                kwargs = ", ".join([f"{k}={v}" for k, v in kwargs.items()])
                logger.log(
                    level,
                    f"Function '{func.__name__}({kwargs})' executed in {elapsed:f} s",
                )
            else:
                logger.log(
                    level, f"Function '{func.__name__}' executed in {elapsed:f} s"
                )
            return result

        return wrapped

    if func and callable(func):
        return decorator(func)
    return decorator


@dataclass
class TranscriptConfig:
    """Config for Transcription Rest API of this project"""

    file_name: str
    API_KEY: str | None = None
    API_REGION: str | None = None
    is_continuous: bool = True
    is_detailed: bool = True
    is_async: bool = False
    is_batched: bool = False
    is_process: bool = True
    verbose: bool = False

    def get_file_format(self) -> str:
        return self.file_name[-3:]

    def get_name(self) -> str:
        return (
            f"is_continuous={self.is_continuous}&"
            f"is_detailed={self.is_detailed}&"
            f"is_batched={self.is_batched}&"
            f"is_async={self.is_async}&"
            f"is_process={self.is_process}&.json"
        )

    def json(self) -> dict[str, str | None]:
        return {
            "is_continuous": str(self.is_continuous),
            "is_detailed": str(self.is_detailed),
            "is_batched": str(self.is_batched),
            "is_async": str(self.is_async),
            "is_process": str(self.is_process),
            "verbose": str(self.verbose),
            "API_KEY": self.API_KEY,
            "API_REGION": self.API_REGION,
        }


def remove_dir(folder: str) -> None:
    # Check Folder is exists or Not
    if os.path.exists(folder):
        # Delete Folder code
        shutil.rmtree(folder)

        # print("The folder has been deleted successfully!")
    # else:
    #     print("Can not delete the folder as it doesn't exists")


def get_first_max_index_key(_array: list[Any], key_elem: Any) -> tuple[int, Any]:
    max_idx = 0
    max_elem = _array[0]
    for idx, elem in enumerate(_array):
        if elem[key_elem] > max_elem[key_elem]:
            max_elem = elem
            max_idx = idx

    return max_idx, max_elem
