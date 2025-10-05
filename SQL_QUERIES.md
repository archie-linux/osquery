## Example SQL Queries

Below are sample queries you can use with Osquery, along with descriptions of what each query does.

---

### **Processes Table Queries**

| Query | Description |
|-------|-------------|
| `SELECT pid, name FROM processes WHERE cpu_usage > 0;` | List active processes using CPU |
| `SELECT pid, name, user FROM processes WHERE user = 'root';` | Find processes owned by root |
| `SELECT pid, name, memory_usage / 1024 / 1024 AS memory_mb FROM processes WHERE memory_usage > 100 * 1024 * 1024;` | Identify high-memory processes (>100MB) |

---

### **Network Connections Table Queries**

| Query | Description |
|-------|-------------|
| `SELECT pid, local_address, local_port, remote_address, remote_port FROM network_connections WHERE protocol = 'TCP';` | List all TCP connections |
| `SELECT pid, local_address, local_port, remote_address FROM network_connections WHERE remote_address = '127.0.0.1';` | Find connections to localhost |
| `SELECT * FROM network_connections WHERE state = 'ESTABLISHED';` | Show all established connections |

---

### **System Info Table Queries**

| Query | Description |
|-------|-------------|
| `SELECT hostname, os_version, cpu_count, memory_total / 1024 / 1024 AS memory_mb, uptime FROM system_info;` | Get detailed system information |
| `SELECT * FROM system_info;` | Get all available system information |

---

### **File Events Table Queries**

| Query | Description |
|-------|-------------|
| `SELECT * FROM file_events;` | List all file change events |
| `SELECT event_type, path, timestamp FROM file_events WHERE event_type = 'modified';` | Show all modified file events |
| `SELECT path, COUNT(*) as changes FROM file_events GROUP BY path ORDER BY changes DESC;` | Find files with the most changes |

---

### **Network Events Table Queries**

| Query | Description |
|-------|-------------|
| `SELECT * FROM network_events;` | List all recorded network events |
| `SELECT laddr, raddr, status, timestamp FROM network_events WHERE status = 'ESTABLISHED';` | Show all established network events |
| `SELECT laddr, COUNT(*) as connections FROM network_events GROUP BY laddr ORDER BY connections DESC;` | Find local addresses with most connections |

---

Copy and paste these queries into the My-Osquery CLI to explore your system!
