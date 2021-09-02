import time
from os.path import dirname
from typing import Callable

from watchdog.observers import Observer

from helpers.FileEventHandler import FileEventHandler


class Watcher:
    def __init__(self, file_path_callback_obj: dict[str, Callable]):
        self.observer = Observer()
        self.file_path_callback_obj = file_path_callback_obj

    def run(self):
        first_file_path = next(iter(self.file_path_callback_obj.keys()))
        directory = dirname(first_file_path)
        event_handler = FileEventHandler(self.file_path_callback_obj)
        self.observer.schedule(event_handler, directory, recursive=False)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()
