"""
Network utilities and socket operations
"""

import socket
import ssl

def create_socket(use_ssl=False, is_udp=False):
    """Create appropriate socket type"""
    if is_udp:
        return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if use_ssl:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        return context.wrap_socket(sock)
    return sock

def test_tcp_connection(target, port, timeout=0.5):
    """Test TCP connection to a port"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((target, port))
        sock.close()
        return result == 0
    except Exception:
        return False

def get_banner(target, port, timeout=1):
    """Get banner from a service"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((target, port))
        banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
        sock.close()
        return banner
    except Exception:
        return ""