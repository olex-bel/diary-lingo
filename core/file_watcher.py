from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent
from typing import Callable

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, on_change_callback: Callable[[], None]) -> None:
        super().__init__()
        self.on_change_callback = on_change_callback

    def on_any_event(self, event: FileSystemEvent) -> None:
        if not event.is_directory:
            self.on_change_callback()

class FileWatcher:
    def __init__(self, directory: str, on_change: Callable[[], None]) -> None:
        self._on_change_callback = on_change
        self.directory = directory
        
        self._observer = Observer()
        self._handler: FileChangeHandler = FileChangeHandler(self._on_change_callback)
        
        self._observer.schedule(self._handler, str(self.directory), recursive=False)
        self._observer.start()
        self._on_change_callback()  # Initial load
    
    def stop(self) -> None:
        if self._observer.is_alive():
            self._observer.stop()
            self._observer.join()
