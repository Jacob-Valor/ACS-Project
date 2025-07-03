"""
TCP-specific scanning functionality
"""

import socket
from datetime import datetime
from colorama import Fore

from scanner.service_detector import ServiceDetector
from config.settings import UTC_PLUS_7
from utils.output import safe_print

def scan_tcp_port(target, port, show_closed, log_manager, stop_event):
    """Scan a single TCP port"""
    if stop_event.is_set():
        return
    
    timestamp = datetime.now(UTC_PLUS_7).strftime("%Y-%m-%d %H:%M:%S UTC+07:00")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((target, port))
        sock.close()
        
        if result == 0:
            service, banner = ServiceDetector.detect_service(target, port, stop_event)
            banner_preview = banner[:100] + "..." if len(banner) > 100 else banner
            banner_preview = banner_preview.replace('\n', ' ').replace('\r', ' ')
            
            safe_print(f"{Fore.GREEN}[{timestamp}] [+] TCP Port {port} is OPEN - Service: {service.upper()}")
            if banner_preview:
                safe_print(f"{Fore.CYAN}    Banner: {banner_preview}")
            
            msg = f"[{timestamp}] {target}:TCP:{port} OPEN | Service: {service} | Banner: {banner}"
            log_manager.log_message(msg)
            
        elif show_closed:
            safe_print(f"{Fore.RED}[{timestamp}] [-] TCP Port {port} is CLOSED")
    
    except Exception as e:
        if not stop_event.is_set():
            safe_print(f"{Fore.YELLOW}[{timestamp}] [!] TCP {port} Error: {e}")