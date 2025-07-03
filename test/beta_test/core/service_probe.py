"""
Service detection and banner grabbing functionality.
"""

import socket
from config.payloads import COMMON_PORTS, SERVICE_PAYLOADS, GENERIC_PAYLOADS
from config.settings import MAX_BANNER_LENGTH, BANNER_TIMEOUT


class ServiceProbe:
    """Handles service detection and banner grabbing."""
    
    def __init__(self, timeout=1.0):
        self.timeout = timeout
    
    def grab_banner(self, sock):
        """Attempt to grab a service banner."""
        try:
            sock.settimeout(BANNER_TIMEOUT)
            banner = sock.recv(MAX_BANNER_LENGTH)
            return banner.decode(errors='ignore').strip()
        except:
            return ''
    
    def probe_service(self, sock, port):
        """Probe a service for identification and banner information."""
        banner = self.grab_banner(sock)
        service = COMMON_PORTS.get(port, 'unknown')
        responses = []
        
        # Try service-specific payloads first
        if service in SERVICE_PAYLOADS:
            payloads = [SERVICE_PAYLOADS[service]]
        else:
            payloads = GENERIC_PAYLOADS
        
        for payload in payloads:
            try:
                sock.sendall(payload)
                sock.settimeout(self.timeout)
                data = sock.recv(MAX_BANNER_LENGTH)
                if data:
                    response = data.decode(errors='ignore').strip()
                    if response and response not in responses:
                        responses.append(response)
            except:
                continue
        
        return banner, responses