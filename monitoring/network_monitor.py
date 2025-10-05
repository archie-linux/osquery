import psutil
import time
from utils import log_results, insert_network_event

def start_network_monitor(stop_event):
    """Monitor active network connections periodically until stop_event is set."""
    seen = set()
    print("Starting network monitor...")
    while not stop_event.is_set():
        try:
            connections = psutil.net_connections()
            for conn in connections:
                if conn.status == psutil.CONN_ESTABLISHED:
                    laddr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A"
                    raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
                    key = (laddr, raddr, conn.status)
                    if key not in seen:
                        event = {
                            "laddr": laddr,
                            "raddr": raddr,
                            "status": conn.status,
                            "timestamp": time.time()
                        }
                        print(f"{laddr} -> {raddr} (Status: {conn.status})")
                        log_results(event, "network_monitor")
                        insert_network_event(event)
                        seen.add(key)
        except psutil.AccessDenied:
            print("Access denied: insufficient permissions to list network connections.")
        except Exception as e:
            print(f"Error occurred: {e}")
        time.sleep(5)
