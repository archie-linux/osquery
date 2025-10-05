# My-Osquery

A simplified Osquery-like tool for macOS, designed for learning purposes. It collects system data (processes, network connections, system info) and supports SQL-like queries using an in-memory SQLite database.

## Features
- **Virtual Tables**: Query system data via `processes`, `network_connections`, and `system_info` tables.
- **SQL-like Interface**: Run SQL queries through a command-line interface (CLI).
- **Real-Time Process Monitoring**: Tracks new processes in the background, logging events to JSON.
- **JSON Logging**: Saves query results and process events to `logs/processes_log.json`.
- **Lightweight Design**: Uses an in-memory database for simplicity and minimal footprint.

## Requirements
- Python 3.8 or higher
- Libraries: `psutil`, `pyyaml` (install via `pip install psutil pyyaml`)
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
   python main.py
   ```

## Usage
Launch the program:
```bash
python main.py
```
The process monitor starts in the background (if `monitor_processes: true` in `config.yaml`), printing new process events to the console and logging them to `logs/processes_log.json`.

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

### Program Output

<pre>
MacBook-Air:my-osquery anish$ python main.py
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
