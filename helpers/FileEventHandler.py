from datetime import datetime, timedelta
from typing import Callable

from watchdog.events import FileSystemEventHandler

from helpers.utils import get_file_last_byte_position, get_file_content_from_byte_position
from models.FileEventHandler import FilePathObj


class FileEventHandler(FileSystemEventHandler):
    def __init__(self, file_path_callback_obj: dict[str, Callable]):
        self.file_path_obj: dict[str, FilePathObj] = {}
        for file_path, callback in file_path_callback_obj.items():
            _dict = {'file_path': file_path, 'callback': callback,
                     'last_byte_position': get_file_last_byte_position(file_path), 'last_modified': datetime.now()}
            obj = FilePathObj(**_dict)
            self.file_path_obj[file_path] = obj

    def on_modified(self, event):
        file_path = event.src_path
        obj = self.file_path_obj.get(file_path)
        if not event.is_directory and obj is not None:
            # Prevent multiple simultaneous calls
            if (datetime.now() - obj.last_modified) < timedelta(milliseconds=10):
                return
            else:
                obj.last_modified = datetime.now()
            content = get_file_content_from_byte_position(obj.file_path, obj.last_byte_position)
            obj.last_byte_position = get_file_last_byte_position(obj.file_path)
            obj.callback(content)
