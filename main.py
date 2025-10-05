import sqlite3
import json
import yaml
import time
import threading
from tables.processes import get_processes
from tables.network import get_network_connections
from tables.system_info import get_system_info
from monitoring.process_monitor import start_process_monitor
# from monitoring.file_monitor import start_file_monitor
from monitoring.network_monitor import start_network_monitor
import os

def setup_database():
    """Set up in-memory SQLite database and populate virtual tables."""
    try:
        conn = sqlite3.connect(':memory:')  # In-memory database
        cursor = conn.cursor()

        # Create tables
        cursor.execute('''
            CREATE TABLE processes (
                pid INTEGER, name TEXT, path TEXT, user TEXT,
                cpu_usage REAL, memory_usage INTEGER, start_time REAL
            )
        ''')
        cursor.execute('''
            CREATE TABLE network_connections (
                pid INTEGER, local_address TEXT, local_port INTEGER,
                remote_address TEXT, remote_port INTEGER, state TEXT, protocol TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE system_info (
                hostname TEXT, os_version TEXT, cpu_count INTEGER,
                memory_total INTEGER, uptime REAL
            )
        ''')

        # Populate tables
        processes = get_processes()
        cursor.executemany('''
            INSERT INTO processes VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', [(p['pid'], p['name'], p['path'], p['user'], p['cpu_usage'], p['memory_usage'], p['start_time'])
              for p in processes])

        connections = get_network_connections()
        cursor.executemany('''
            INSERT INTO network_connections VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', [(c['pid'], c['local_address'], c['local_port'], c['remote_address'], c['remote_port'], c['state'], c['protocol'])
              for c in connections])

        system_info = get_system_info()
        cursor.executemany('''
            INSERT INTO system_info VALUES (?, ?, ?, ?, ?)
        ''', [(s['hostname'], s['os_version'], s['cpu_count'], s['memory_total'], s['uptime'])
              for s in system_info])

        conn.commit()
        return conn, cursor
    except sqlite3.Error as e:
        print(f"Database setup error: {e}")
        raise

def log_results(results, table_name):
    """Log query results and monitoring events to a JSON file."""
    try:
        # Ensure logs directory exists
        os.makedirs('logs', exist_ok=True)

        # Special handling for monitoring events
        if table_name == 'file_monitor':
            log_file = 'logs/file_monitor_log.json'
        elif table_name == 'network_monitor':
            log_file = 'logs/network_monitor_log.json'
        else:
            log_file = f'logs/{table_name}_log.json'

        with open(log_file, 'a') as f:
            json.dump(results, f, indent=2)
            f.write('\n')
    except IOError as e:
        print(f"Error writing to log file: {e}")

def run_query(cursor, query, table_name):
    """Execute a SQL query and return results."""
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        log_results(results, table_name)
        return results
    except sqlite3.Error as e:
        print(f"Query error: {e}")
        return []

def main():
    """Main CLI loop for querying tables."""
    try:
        # Load configuration
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)
    except (IOError, yaml.YAMLError) as e:
        print(f"Error loading config.yaml: {e}")
        return

    # Set up database
    try:
        conn, cursor = setup_database()
    except Exception as e:
        print(f"Failed to set up database: {e}")
        return

    # Event to stop background threads
    stop_event = threading.Event()

    # Start process monitor in background
    if config.get('monitor_processes', False):
        print("Starting process monitor in background...")
        monitor_thread = threading.Thread(target=start_process_monitor, args=(stop_event,))
        monitor_thread.daemon = True  # Exit thread when main program exits
        monitor_thread.start()

    # Start file monitor(s) in background for each directory in config
    file_monitor_config = config.get('monitor_files', {})
    if file_monitor_config.get('enabled', False):
        # Import here to avoid circular import
        from monitoring.file_monitor import start_file_monitor
        directories = file_monitor_config.get('directories', [])
        if not directories:
            print("No directories specified for file monitoring.")
        else:
            for directory in directories:
                print(f"Starting file monitor in background for {directory}...")
                file_thread = threading.Thread(target=start_file_monitor, args=(stop_event, directory))
                file_thread.daemon = True
                file_thread.start()


    # Start network monitor in background
    if config.get('monitor_network', False):
        print("Starting network monitor in background...")
        network_monitor_thread = threading.Thread(target=start_network_monitor, args=(stop_event,))
        network_monitor_thread.daemon = True
        network_monitor_thread.start()

    # CLI loop
    print("Welcome to My-Osquery! Enter SQL queries or 'exit' to quit.")
    while True:
        try:
            query = input("SQL> ")
            if query.lower() == 'exit':
                break
            # Determine table for logging (simplistic approach)
            table_name = 'unknown'
            for table in ['processes', 'network_connections', 'system_info']:
                if table in query.lower():
                    table_name = table
                    break
            results = run_query(cursor, query, table_name)
            for row in results:
                print(row)
        except KeyboardInterrupt:
            print("\nInterrupted, exiting...")
            break
        except Exception as e:
            print(f"Error processing query: {e}")

    # Signal background threads to stop
    stop_event.set()
    # Give a moment for threads to clean up
    time.sleep(1)

    # Close database connection
    try:
        conn.close()
        print("Database connection closed.")
    except sqlite3.Error as e:
        print(f"Error closing database: {e}")

if __name__ == '__main__':
    main()
