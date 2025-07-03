"""
Core scanning functionality
"""

import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Thread, Event

from colorama import Fore
from scanner.protocols.tcp import scan_tcp_port
from scanner.protocols.udp import scan_udp_port
from utils.logger import LogManager
from utils.output import safe_print

class PortScanner:
    """Main port scanner class"""
    
    def __init__(self, target, ports, max_threads=100, show_closed=False, 
                 log_file="scan_results.log", udp_mode=False):
        self.target = target
        self.ports = ports
        self.max_threads = max_threads
        self.show_closed = show_closed
        self.log_file = log_file
        self.udp_mode = udp_mode
        self.stop_event = Event()
        self.log_manager = LogManager(log_file)
        
    def run(self):
        """Execute the port scan"""
        start_time = time.time()
        
        self._show_scan_info()
        
        # Start logger thread
        logger_thread = Thread(target=self.log_manager.log_writer, daemon=True)
        logger_thread.start()
        
        try:
            self._execute_scan()
        except KeyboardInterrupt:
            self.stop_event.set()
            safe_print(f"\n{Fore.YELLOW}[!] Scan interrupted by user")
        except Exception as e:
            safe_print(f"{Fore.RED}[!] Scan error: {e}")
            self.stop_event.set()
        finally:
            self._cleanup(start_time, logger_thread)
    
    def _show_scan_info(self):
        """Display scan information"""
        safe_print(f"{Fore.CYAN}[+] Starting advanced port scan on {self.target}")
        safe_print(f"[+] Scanning {len(self.ports)} ports with {self.max_threads} threads")
        safe_print(f"[+] Protocol detection enabled for 16 services")
        safe_print(f"[+] Scan type: {'UDP' if self.udp_mode else 'TCP'}")
    
    def _execute_scan(self):
        """Execute the actual scanning with thread pool"""
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = []
            
            for port in self.ports:
                if self.stop_event.is_set():
                    break
                
                scan_func = scan_udp_port if self.udp_mode else scan_tcp_port
                future = executor.submit(
                    scan_func,
                    self.target, 
                    port, 
                    self.show_closed,
                    self.log_manager,
                    self.stop_event
                )
                futures.append(future)
            
            # Process results
            for future in as_completed(futures):
                if self.stop_event.is_set():
                    break
                try:
                    future.result()
                except Exception as e:
                    safe_print(f"{Fore.RED}[!] Thread error: {e}")
    
    def _cleanup(self, start_time, logger_thread):
        """Clean up resources and show results"""
        elapsed_time = time.time() - start_time
        minutes, seconds = divmod(elapsed_time, 60)
        safe_print(f"\n{Fore.CYAN}[*] Scan completed in {int(minutes)}m {seconds:.2f}s")
        safe_print(f"[*] Results saved to: {self.log_file}")
        
        # Clean up logger
        self.log_manager.stop()
        logger_thread.join(timeout=2)
    
    def stop(self):
        """Stop the scanner"""
        self.stop_event.set()
        if hasattr(self, 'log_manager'):
            self.log_manager.stop()