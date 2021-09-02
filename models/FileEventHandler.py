from datetime import datetime
from typing import Callable

from pydantic import BaseModel


class FilePathObj(BaseModel):
    file_path: str
    callback: Callable
    last_modified: datetime
    last_byte_position: int
