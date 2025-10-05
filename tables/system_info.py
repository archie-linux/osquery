import platform
import psutil
import time

def get_system_info():
    """Fetch system information for the system_info table."""
    try:
        return [{
            'hostname': platform.node(),
            'os_version': platform.mac_ver()[0],
            'cpu_count': psutil.cpu_count(),
            'memory_total': psutil.virtual_memory().total,
            'uptime': time.time() - psutil.boot_time()
        }]
    except Exception as e:
        print(f"Error fetching system info: {e}")
        return []
