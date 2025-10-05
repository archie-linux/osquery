import psutil
import time
import json

def start_process_monitor(stop_event):
    """Monitor new processes and log them until stop_event is set."""
    known_pids = set()
    while not stop_event.is_set():
        try:
            current_pids = {p.pid for p in psutil.process_iter()}
            new_pids = current_pids - known_pids
            for pid in new_pids:
                try:
                    proc = psutil.Process(pid)
                    event = {
                        'pid': pid,
                        'name': proc.name(),
                        'timestamp': time.time()
                    }
                    print(f"New process: {event['name']} (PID: {pid})")
                    with open('logs/processes_log.json', 'a') as f:
                        json.dump(event, f)
                        f.write('\n')
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            known_pids.update(new_pids)
            time.sleep(1)
        except Exception as e:
            print(f"Error in process monitor: {e}")
            time.sleep(1)
