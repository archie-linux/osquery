from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os
import sys


class ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(f"File modified: {event.src_path}")

    def on_created(self, event):
        print(f"File created: {event.src_path}")

    def on_deleted(self, event):
        print(f"File deleted: {event.src_path}")

def start_file_monitor(stop_event, path):
    """Monitor file changes in the given directory."""
    print(f"Starting file monitor on {path}...")
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while not stop_event.is_set():
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()
