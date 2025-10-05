import os
import json
import threading

db_cursor = None
db_lock = threading.Lock()

def set_db_cursor(cursor):
    global db_cursor
    db_cursor = cursor

def log_results(results, table_name):
    """Log query results and monitoring events to a JSON file."""
    try:
        os.makedirs('logs', exist_ok=True)
        if table_name == 'file_monitor':
            log_file = 'logs/file_monitor_log.json'
        elif table_name == 'network_monitor':
            log_file = 'logs/network_monitor_log.json'
        elif table_name == 'processes':
            log_file = 'logs/processes_log.json'
        else:
            log_file = f'logs/{table_name}_log.json'
        with open(log_file, 'a') as f:
            json.dump(results, f, indent=2)
            f.write('\n')
    except IOError as e:
        print(f"Error writing to log file: {e}")

def insert_file_event(event):
    if db_cursor is None:
        return
    with db_lock:
        db_cursor.execute(
            "INSERT OR IGNORE INTO file_events (event_type, path, timestamp) VALUES (?, ?, ?)",
            (event['event'], event['path'], event['timestamp'])
        )

def insert_network_event(event):
    if db_cursor is None:
        return
    with db_lock:
        db_cursor.execute(
            "INSERT OR IGNORE INTO network_events (laddr, raddr, status, timestamp) VALUES (?, ?, ?, ?)",
            (event['laddr'], event['raddr'], event['status'], event['timestamp'])
        )

def insert_process_event(event):
    if db_cursor is None:
        return
    with db_lock:
        db_cursor.execute(
            "INSERT OR IGNORE INTO process_events (pid, name, action, timestamp) VALUES (?, ?, ?, ?)",
            (event['pid'], event['name'], event['action'], event['timestamp'])
        )
