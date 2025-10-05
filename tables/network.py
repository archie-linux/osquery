import psutil

def get_network_connections():
    """Fetch network connection data for the network_connections table."""
    connections = []
    try:
        for conn in psutil.net_connections(kind='inet'):
            connections.append({
                'pid': conn.pid if conn.pid is not None else -1,
                'local_address': conn.laddr.ip,
                'local_port': conn.laddr.port,
                'remote_address': conn.raddr.ip if conn.raddr else '',
                'remote_port': conn.raddr.port if conn.raddr else 0,
                'state': conn.status,
                'protocol': 'TCP' if conn.type == 1 else 'UDP'
            })
    except Exception as e:
        print(f"Error fetching network connections: {e}")
    return connections
