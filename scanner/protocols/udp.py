"""
UDP-specific scanning functionality
"""

import socket
from datetime import datetime
from colorama import Fore

from scanner.service_detector import ServiceDetector
from scanner.protocols.config import SERVICE_PAYLOADS
from config.settings import UTC_PLUS_7
from utils.output import safe_print

def scan_udp_port(target, port, show_closed, log_manager, stop_event):
    """Scan a single UDP port"""
    if stop_event.is_set():
        return
    
    timestamp = datetime.now(UTC_PLUS_7).strftime("%Y-%m-%d %H:%M:%S UTC+07:00")
    
    try:
        # Try DNS first for port 53
        if port == 53:
            success, response = ServiceDetector._test_service(target, port, 'dns', SERVICE_PAYLOADS['dns'])
            if success:
                safe_print(f"{Fore.CYAN}[{timestamp}] [+] UDP Port {port} is OPEN - Service: DNS")
                msg = f"[{timestamp}] {target}:UDP:{port} OPEN | Service: DNS | Response: {response}"
                log_manager.log_message(msg)
                return
        
        # Try SNMP for port 161
        if port == 161:
            success, response = ServiceDetector._test_service(target, port, 'snmp', SERVICE_PAYLOADS['snmp'])
            if success:
                safe_print(f"{Fore.CYAN}[{timestamp}] [+] UDP Port {port} is OPEN - Service: SNMP")
                msg = f"[{timestamp}] {target}:UDP:{port} OPEN | Service: SNMP | Response: {response}"
                log_manager.log_message(msg)
                return
        
        # Generic UDP probe
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(1)
        sock.sendto(b'\x00', (target, port))
        
        try:
            data, _ = sock.recvfrom(1024)
            response = data.decode('utf-8', errors='ignore').strip()
            safe_print(f"{Fore.CYAN}[{timestamp}] [+] UDP Port {port} is OPEN | Response: {response[:50]}...")
            msg = f"[{timestamp}] {target}:UDP:{port} OPEN | Response: {response}"
            log_manager.log_message(msg)
        except socket.timeout:
            if show_closed:
                safe_print(f"{Fore.MAGENTA}[{timestamp}] [-] UDP Port {port} is CLOSED/Filtered")
        
        sock.close()
    
    except Exception as e:
        if not stop_event.is_set():
            safe_print(f"{Fore.YELLOW}[{timestamp}] [!] UDP {port} Error: {e}")