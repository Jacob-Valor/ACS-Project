"""
Main port scanner implementation.
"""

import time
import socket
from threading import Thread, Event
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style

from config.settings import UTC_PLUS_7
from core.service_probe import ServiceProbe
from utils.logger import Logger
from utils.colors import format_timestamp


class PortScanner:
    """Advanced port scanner with TCP/UDP support and service detection."""
    
    def __init__(self, target, ports, max_threads=100, show_closed=False, 
                 log_file="scan_results.log", udp_mode=False, timeout=0.5):
        self.target = target
        self.ports = ports
        self.max_threads = max_threads
        self.show_closed = show_closed
        self.log_file = log_file
        self.udp_mode = udp_mode
        self.timeout = timeout
        self.stop_event = Event()
        
        # Initialize components
        self.logger = Logger(log_file)
        self.service_probe = ServiceProbe(timeout)
        
    def scan_tcp_port(self, port):
        """Scan a single TCP port."""
        if self.stop_event.is_set():
            return
            
        timestamp = format_timestamp()
        
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.timeout)
                result = sock.connect_ex((self.target, port))
                
                if result == 0:
                    print(f"{Fore.GREEN}[{timestamp}] [+] TCP Port {port} is OPEN")
                    
                    # Perform service detection
                    banner, responses = self.service_probe.probe_service(sock, port)
                    
                    # Log the result
                    log_msg = f"[{timestamp}] {self.target}:TCP:{port} OPEN"
                    if banner:
                        log_msg += f" | Banner: {banner}"
                    if responses:
                        log_msg += f" | Responses: {responses}"
                    
                    self.logger.log(log_msg)
                    
                elif self.show_closed:
                    print(f"{Fore.RED}[{timestamp}] [-] TCP Port {port} is CLOSED")
                    
        except Exception as e:
            if not self.stop_event.is_set():
                print(f"{Fore.YELLOW}[{timestamp}] [!] TCP {port} Error: {e}")
    
    def scan_udp_port(self, port):
        """Scan a single UDP port."""
        if self.stop_event.is_set():
            return
            
        timestamp = format_timestamp()
        
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.settimeout(1.0)  # UDP needs longer timeout
                sock.sendto(b'\x00', (self.target, port))
                
                try:
                    data, _ = sock.recvfrom(1024)
                    response = data.decode(errors='ignore').strip()
                    print(f"{Fore.CYAN}[{timestamp}] [+] UDP Port {port} is OPEN | Response: {response}")
                    
                    log_msg = f"[{timestamp}] {self.target}:UDP:{port} OPEN | Data: {response}"
                    self.logger.log(log_msg)
                    
                except socket.timeout:
                    if self.show_closed:
                        print(f"{Fore.MAGENTA}[{timestamp}] [-] UDP Port {port} is CLOSED/Filtered")
                        
        except Exception as e:
            if not self.stop_event.is_set():
                print(f"{Fore.YELLOW}[{timestamp}] [!] UDP {port} Error: {e}")
    
    def run(self):
        """Execute the port scan."""
        start_time = time.time()
        
        print(f"[+] Scanning {self.target} on {len(self.ports)} ports with {self.max_threads} threads")
        print(f"[+] Mode: {'UDP' if self.udp_mode else 'TCP'}")
        print(f"[+] Timeout: {self.timeout}s")
        print(f"[+] Log file: {self.log_file}")
        print()
        
        # Start logger thread
        logger_thread = Thread(target=self.logger.writer_loop, daemon=True)
        logger_thread.start()
        
        try:
            with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
                # Submit all port scans
                scan_function = self.scan_udp_port if self.udp_mode else self.scan_tcp_port
                futures = [executor.submit(scan_function, port) for port in self.ports]
                
                # Process completed scans
                for future in as_completed(futures):
                    if self.stop_event.is_set():
                        break
                    try:
                        future.result()
                    except Exception as e:
                        print(f"{Fore.RED}[!] Scan error: {e}{Style.RESET_ALL}")
                        
        except KeyboardInterrupt:
            self.stop_event.set()
            print(f"\n{Fore.YELLOW}[!] Shutting down gracefully...{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[!] Error during scan: {e}{Style.RESET_ALL}")
            self.stop_event.set()
        
        # Calculate and display elapsed time
        elapsed_time = time.time() - start_time
        minutes, seconds = divmod(elapsed_time, 60)
        print(f"\n{Fore.CYAN}[*] Scan completed in {int(minutes)}m {seconds:.2f}s{Style.RESET_ALL}")
        
        # Clean up logger
        self.logger.stop()
        logger_thread.join(timeout=2)