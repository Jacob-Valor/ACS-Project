"""
SSL/TLS utilities for secure connections
"""

import ssl
import socket
from datetime import datetime

def create_ssl_context(verify_certs=False):
    """Create SSL context for secure connections"""
    context = ssl.create_default_context()
    if not verify_certs:
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
    return context

def get_ssl_cert_info(target, port, timeout=2):
    """Get SSL certificate information"""
    try:
        context = create_ssl_context(verify_certs=True)
        with socket.create_connection((target, port), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=target) as ssock:
                cert = ssock.getpeercert()
                return {
                    'subject': cert.get('subject', []),
                    'issuer': cert.get('issuer', []),
                    'version': cert.get('version', 'Unknown'),
                    'serial_number': cert.get('serialNumber', 'Unknown'),
                    'not_before': cert.get('notBefore', 'Unknown'),
                    'not_after': cert.get('notAfter', 'Unknown'),
                    'san': cert.get('subjectAltName', [])
                }
    except Exception as e:
        return {'error': str(e)}

def test_ssl_connection(target, port, timeout=2):
    """Test SSL connection to a port"""
    try:
        context = create_ssl_context(verify_certs=False)
        with socket.create_connection((target, port), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=target) as ssock:
                return True, ssock.version()
    except Exception as e:
        return False, str(e)