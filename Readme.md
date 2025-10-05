# My-Osquery

My-Osquery is ironically built for your endpoints that collects system data (processes, network connections, system info) and supports SQL-like queries using an in-memory SQLite database.

## Features
- **Virtual Tables**: Query system data via `processes`, `network_connections`, and `system_info` tables.
- **SQL-like Interface**: Run SQL queries through a command-line interface (CLI).
- **Real-Time Process Monitoring**: Tracks new processes in the background, logging events to JSON.
- **JSON Logging**: Saves query results and process events to `logs/processes_log.json`.
- **Lightweight Design**: Uses an in-memory database for simplicity and minimal footprint.

## Requirements
- Python 3.8 or higher
- Libraries: `psutil`, `pyyaml` `watchdog` (install via `pip install psutil pyyaml watchdog`)
- macOS with appropriate permissions (e.g., Full Disk Access for Terminal)

## Setup

1. **Install Dependencies**:
   ```bash
   pip install psutil pyyaml

2. **Create Logs Directory**:
   ```bash
   mkdir logs
   ```

3. **Verify Configuration**:
   Ensure `config.yaml` exists in the project root with:
   ```yaml
   monitor_processes: true
   log_path: logs/
   ```
4. **Run the Program**:
   ```bash
   sudo python main.py
   ```

## Usage
Launch the program:
```bash
sudo python main.py
```
The process monitor starts in the background (if `monitor_processes: true` in `config.yaml`), printing new process events to the console and logging them to `logs/processes_log.json`.

If you enable `file_monitor: true` in `config.yaml`, a file monitor will also run in the background. It uses the `watchdog` library to watch for file creation, modification, and deletion events in specified directories (configured in `config.yaml`). Detected file events are printed to the console and logged to `logs/file_events_log.json`.

Similarly, enabling `network_monitor: true` in `config.yaml` starts a network monitor. This component periodically scans active network connections using `psutil`, detects new or closed connections, and logs these events to `logs/network_events_log.json`.

**How it works behind the scenes:**
- Each monitor (process, file, network) runs in its own background thread.
- The process monitor polls the system for new processes and logs any that appear since the last check.
- The file monitor uses OS-level notifications (via `watchdog`) to efficiently detect file system changes in real time.
- The network monitor periodically checks the list of active network connections and logs any changes.
- All monitors write structured JSON logs for easy parsing and analysis.

At the `SQL>` prompt, enter SQL queries, for example:
```sql
SELECT pid, name FROM processes WHERE cpu_usage > 0;
```
Type `exit` to quit the program.

Check `logs/processes_log.json` for query results and process events.

**Note**: The database is in-memory, so data is not saved to disk and is only accessible via the CLI during program execution.

## Example SQL Queries
Use these queries to explore the virtual tables:

### Processes Table
- List processes with CPU usage:
  ```sql
  SELECT pid, name, cpu_usage FROM processes WHERE cpu_usage > 0;
  ```

- Find processes owned by root:
  ```sql
  SELECT pid, name, user FROM processes WHERE user = 'root';
  ```

- Identify high-memory processes (> 100 MB):
  ```sql
  SELECT pid, name, memory_usage / 1024 / 1024 AS memory_mb FROM processes WHERE memory_usage > 100 * 1024 * 1024;
  ```

### Network Connections Table
- List TCP connections:
  ```sql
  SELECT pid, local_address, local_port, remote_address, remote_port FROM network_connections WHERE protocol = 'TCP';
  ```

- Find connections to localhost:
  ```sql
  SELECT pid, local_address, local_port, remote_address FROM network_connections WHERE remote_address = '127.0.0.1';
  ```

- Show established connections:
  ```sql
  SELECT * FROM network_connections WHERE state = 'ESTABLISHED';
  ```

### System Info Table
- Get system details:
  ```sql
  SELECT hostname, os_version, cpu_count, memory_total / 1024 / 1024 AS memory_mb, uptime FROM system_info;
  ```

## Triggering File and Network Monitor Events

To test and see file and network monitor events in action, you can manually create file changes and network connections. Here are example steps:

### 1. Trigger a File Change Event

With file monitoring enabled and `/etc` in your `config.yaml` directories, run:

```bash
# Create a new file in /etc (requires sudo)
sudo touch /etc/test_osquery.txt

# Modify the file
sudo echo "test" >> /etc/test_osquery.txt

# Delete the file
sudo rm /etc/test_osquery.txt
```

You should see corresponding "File created", "File modified", and "File deleted" events printed in the console and logged in `logs/file_events_log.json`.

---

### 2. Trigger a Network Connection Event

With network monitoring enabled, open a new terminal and run:

```bash
# Start a simple TCP server (in one terminal)
nc -l 12345

# Connect to it from another terminal
nc localhost 12345
```

This will create a new network connection, which should be detected by the network monitor. You should see "Active connections" count change in the console and new events in `logs/network_events_log.json`.


### Program Output

<pre>
MacBook-Air:my-osquery anish$ sudo python main.py
Error fetching network connections: (pid=63107)
Starting process monitor in background...
New process: kernel_task (PID: 0)
Welcome to My-Osquery! Enter SQL queries or 'exit' to quit.
SQL> New process: launchd (PID: 1)
New process: routined (PID: 51215)
New process: VTDecoderXPCService (PID: 83983)
New process: userfsd (PID: 50203)
New process: userfs_helper (PID: 50205)
New process: helpd (PID: 67614)
New process: XProtect (PID: 29726)
New process: PlugInLibrarySer (PID: 50209)
New process: proactiveeventtrackerd (PID: 22569)
New process: deleted_helper (PID: 86058)
New process: TextInputSwitcher (PID: 1065)
New process: replayd (PID: 86060)
New process: AssetCache (PID: 86061)
New process: ssh-agent (PID: 47150)
New process: geodMachServiceBridge (PID: 86062)
New process: installd (PID: 86063)
New process: cloudd (PID: 86064)
New process: system_installd (PID: 86065)
New process: spindump (PID: 11327)
New process: ssh-agent (PID: 66627)
New process: ssh-agent (PID: 83014)
New process: aned (PID: 33871)
...
...
...
SQL>
SQL> SELECT pid, name, user FROM processes WHERE user = 'root'
(0, 'kernel_task', 'root')
(1, 'launchd', 'root')
(319, 'logd', 'root')
(321, 'UserEventAgent', 'root')
(323, 'uninstalld', 'root')
(324, 'fseventsd', 'root')
(325, 'mediaremoted', 'root')
(328, 'systemstats', 'root')
(330, 'configd', 'root')
(332, 'powerd', 'root')
(333, 'IOMFB_bics_daemo', 'root')
(338, 'remoted', 'root')
(343, 'watchdogd', 'root')
(347, 'mds', 'root')
(349, 'kernelmanagerd', 'root')
(350, 'diskarbitrationd', 'root')
(354, 'syslogd', 'root')
(357, 'thermalmonitord', 'root')
(358, 'opendirectoryd', 'root')
(359, 'apsd', 'root')
(360, 'launchservicesd', 'root')
...
...
...
New process: online-authd (PID: 53145)
New process: bash (PID: 99233)
New process: ControlCenterHelper (PID: 29603)
New process: com.apple.SafariPlatformSupport.Helper (PID: 29604)
New process: cloudphotod (PID: 8105)
New process: splunkd (PID: 950)
New process: splunkd (PID: 951)
New process: DiskUnmountWatcher (PID: 9151)
New process: passd (PID: 69580)
New process: Code Helper (GPU) (PID: 97277)
New process: ssh-agent (PID: 53205)
New process: simdiskimaged (PID: 69596)
New process: ssh-agent (PID: 29663)
New process: distnoted (PID: 69602)
New process: ssh-agent (PID: 49127)
New process: distnoted (PID: 1001)
New process: distnoted (PID: 1002)
New process: ssh-agent (PID: 89065)
New process: nc (PID: 52212)
New process: mdbulkimport (PID: 1013)
New process: IMAutomaticHistoryDeletionAgent (PID: 11255)
New process: IOUserBluetoothSerialDriver (PID: 11256)
New process: IOUserBluetoothSerialDriver (PID: 11257)
New process: Electron (PID: 97274)
New process: chrome_crashpad_handler (PID: 97276)
New process: nc (PID: 52221)
New process: Code Helper (PID: 97278)
New process: amsaccountsd (PID: 54704)
New process: amsengagementd (PID: 54705)
New process: syncdefaultsd (PID: 54706)
New process: swcd (PID: 54707)
Active connections: 7
127.0.0.1:55151 -> 127.0.0.1:8000 (Status: ESTABLISHED)
127.0.0.1:8000 -> 127.0.0.1:55151 (Status: ESTABLISHED)
192.168.29.79:55042 -> 51.132.193.104:443 (Status: ESTABLISHED)
2405:201:8:7832:f871:928f:722c:bcf9:52010 -> 2404:6800:4003:c00::bc:5228 (Status: ESTABLISHED)
192.168.29.79:54641 -> 140.82.114.26:443 (Status: ESTABLISHED)
127.0.0.1:49154 -> 127.0.0.1:9997 (Status: ESTABLISHED)
127.0.0.1:9997 -> 127.0.0.1:49154 (Status: ESTABLISHED)
Active connections: 8
127.0.0.1:55151 -> 127.0.0.1:8000 (Status: ESTABLISHED)
127.0.0.1:8000 -> 127.0.0.1:55151 (Status: ESTABLISHED)
192.168.29.79:55042 -> 51.132.193.104:443 (Status: ESTABLISHED)
2405:201:8:7832:f871:928f:722c:bcf9:52010 -> 2404:6800:4003:c00::bc:5228 (Status: ESTABLISHED)
192.168.29.79:54641 -> 140.82.114.26:443 (Status: ESTABLISHED)
192.168.29.79:55306 -> 162.159.140.229:443 (Status: ESTABLISHED)
127.0.0.1:49154 -> 127.0.0.1:9997 (Status: ESTABLISHED)
127.0.0.1:9997 -> 127.0.0.1:49154 (Status: ESTABLISHED)
Active connections: 5
192.168.29.79:55042 -> 51.132.193.104:443 (Status: ESTABLISHED)
2405:201:8:7832:f871:928f:722c:bcf9:52010 -> 2404:6800:4003:c00::bc:5228 (Status: ESTABLISHED)
192.168.29.79:54641 -> 140.82.114.26:443 (Status: ESTABLISHED)
127.0.0.1:49154 -> 127.0.0.1:9997 (Status: ESTABLISHED)
127.0.0.1:9997 -> 127.0.0.1:49154 (Status: ESTABLISHED)
File created: /private/etc/test.txt
File modified: /private/etc
File deleted: /private/etc/test.txt
File modified: /private/etc
</pre>

### Logs: processes_log.json

<pre>

{"pid": 0, "name": "kernel_task", "timestamp": 1747508741.405966}
{"pid": 1, "name": "launchd", "timestamp": 1747508741.406204}
{"pid": 51215, "name": "routined", "timestamp": 1747508741.4062898}
{"pid": 83983, "name": "VTDecoderXPCService", "timestamp": 1747508741.406392}
{"pid": 71701, "name": "Python", "timestamp": 1747508741.406463}
{"pid": 50203, "name": "userfsd", "timestamp": 1747508741.4065301}
{"pid": 50205, "name": "userfs_helper", "timestamp": 1747508741.4065988}
{"pid": 67614, "name": "helpd", "timestamp": 1747508741.406663}
{"pid": 29726, "name": "XProtect", "timestamp": 1747508741.406726}
{"pid": 50209, "name": "PlugInLibrarySer", "timestamp": 1747508741.406802}
{"pid": 22569, "name": "proactiveeventtrackerd", "timestamp": 1747508741.40689}
{"pid": 86058, "name": "deleted_helper", "timestamp": 1747508741.406958}
{"pid": 1065, "name": "TextInputSwitcher", "timestamp": 1747508741.4070349}
{"pid": 86060, "name": "replayd", "timestamp": 1747508741.407098}
</pre>
