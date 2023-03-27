"""module for producing mock response
"""

import json
import os
import pkgutil
from copy import deepcopy
from typing import Any


# This method will be used by the mock to replace requests.get
def mocked_requests_get(*args: Any, **kwargs: Any) -> Any:
    assert not kwargs, "Only positional argument must be used"

    transcript_config = deepcopy(args[0])
    transcript_config.is_process = False
    file_name = os.path.basename(transcript_config.file_name)

    data_str: Any = pkgutil.get_data(
        __name__, f"data/{file_name}/{transcript_config.get_name()}"
    )
    data_str = "" if data_str is None else data_str.decode("utf-8")
    data = json.loads(data_str)[0]
    data[1] = tuple(data[1])
    data = tuple(data)
    return data
