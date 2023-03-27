from __future__ import annotations

from enum import Enum, unique


@unique
class DataDirs(str, Enum):
    """Enum containig important directory names"""

    TEMP_DIR = "temp_data"
    MOCK_DIR = "tests/fixture/data"

    def __str__(self) -> str:
        return str(self.value)


@unique
class PathParams(str, Enum):
    """Enum containig important directory names"""

    CREATE_GAMELOG = "create_record"
    CREATE_TEAMSTAT = "create_teamstat"
    GET_GAMELOG = "get_gamelog"
    GET_TEAMSTAT = "get_teamstat"
    PREDICT = "predict_game"

    def __str__(self) -> str:
        return str(self.value)
