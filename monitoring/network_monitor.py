import psutil
import time
import logging
import json
import os

def start_network_monitor(stop_event):
    """Monitor active network connections periodically until stop_event is set."""

    logging.info("Starting network monitor...")
    while not stop_event.is_set():
        try:
            connections = psutil.net_connections()
            active_connections = [
                conn for conn in connections
                if conn.status == psutil.CONN_ESTABLISHED
            ]
            print(f"Active connections: {len(active_connections)}")
            for conn in active_connections:
                laddr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A"
                raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
                print(f"{laddr} -> {raddr} (Status: {conn.status})")
        except psutil.AccessDenied:
            print("Access denied: insufficient permissions to list network connections.")
        except Exception as e:
            print(f"Error occurred: {e}")
        time.sleep(5)
