import psutil

def get_processes():
    """Fetch process data for the processes table."""
    processes = []
    try:
        for proc in psutil.process_iter(['pid', 'name', 'exe', 'username', 'cpu_percent', 'memory_info', 'create_time']):
            try:
                processes.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'path': proc.info['exe'] or '',
                    'user': proc.info['username'] or '',
                    'cpu_usage': proc.info['cpu_percent'],
                    'memory_usage': proc.info['memory_info'].rss if proc.info['memory_info'] else 0,
                    'start_time': proc.info['create_time']
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    except Exception as e:
        print(f"Error fetching processes: {e}")
    return processes
