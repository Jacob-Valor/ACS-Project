"""
Service detection functionality
"""

import socket
from .protocols.config import SERVICE_PAYLOADS, COMMON_PORTS
from .network_utils import create_socket

class ServiceDetector:
    """Service detection and banner grabbing"""
    
    @staticmethod
    def detect_service(target, port, stop_event):
        """Detect service running on a port"""
        if stop_event.is_set():
            return "unknown", ""
        
        # Check if it's a common port first
        if port in COMMON_PORTS:
            service_name = COMMON_PORTS[port]
            if service_name in SERVICE_PAYLOADS:
                success, response = ServiceDetector._test_service(
                    target, port, service_name, SERVICE_PAYLOADS[service_name]
                )
                if success:
                    return service_name, response
        
        # Try all services if common port detection failed
        for service_name, config in SERVICE_PAYLOADS.items():
            if stop_event.is_set():
                break
            
            success, response = ServiceDetector._test_service(
                target, port, service_name, config
            )
            if success:
                return service_name, response
        
        # If no service detected, try to get basic banner
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect((target, port))
            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            sock.close()
            return "unknown", banner
        except:
            return "unknown", ""
    
    @staticmethod
    def _test_service(target, port, service_name, config):
        """Test a specific service on a port"""
        try:
            is_udp = config.get('udp', False)
            use_ssl = config.get('ssl', False)
            
            sock = create_socket(use_ssl, is_udp)
            sock.settimeout(2)
            
            if is_udp:
                sock.sendto(config['payload'], (target, port))
                try:
                    data, _ = sock.recvfrom(1024)
                    response = data
                except socket.timeout:
                    return False, ""
            else:
                sock.connect((target, port))
                
                # Get initial banner
                banner = b""
                try:
                    banner = sock.recv(1024)
                except socket.timeout:
                    pass
                
                # Send payload if specified
                if config['payload']:
                    payload = config['payload']
                    if b'{host}' in payload:
                        payload = payload.replace(b'{host}', target.encode())
                    sock.sendall(payload)
                    
                    try:
                        response = sock.recv(1024)
                    except socket.timeout:
                        response = b""
                else:
                    response = banner
            
            sock.close()
            
            # Check if response matches expected patterns
            response_lower = response.lower()
            for expected in config['expected']:
                if expected.lower() in response_lower:
                    return True, response.decode('utf-8', errors='ignore')
            
            return False, response.decode('utf-8', errors='ignore')
        
        except Exception as e:
            return False, str(e)