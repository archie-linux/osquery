from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os
from utils import log_results, insert_file_event

class ChangeHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory:
            return
        event_type = event.event_type
        event_data = {
            "event": event_type,
            "path": event.src_path,
            "timestamp": time.time()
        }
        print(f"File {event_type}: {event.src_path}")
        log_results(event_data, "file_monitor")
        insert_file_event(event_data)

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
