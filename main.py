#!/usr/bin/env python3

"""
Advanced Multi-Protocol Port Scanner with Service Detection
Entry point and command-line interface
"""

import os
import sys
import argparse
from datetime import datetime, timezone, timedelta
from colorama import Fore, Style, init

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root) if project_root not in sys.path else None

# Local imports
from scanner.core import PortScanner
from utils.output import safe_print
from utils.port_parser import parse_ports
from config.settings import UTC_PLUS_7

# Initialize colorama
init(autoreset=True)

def create_parser():
    parser = argparse.ArgumentParser(
        description="Advanced Multi-Protocol Port Scanner with Service Detection",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py -t 192.168.1.1 -p 80,443,22
  python main.py -t example.com -p 1-1000 --threads 200
  python main.py -t 10.0.0.1 -p all --udp
  python main.py -t target.com -p 21,22,23,25,53,80,110,143,443,445,3389,5900,3306,5432,6379,161

Supported Protocols:
  HTTP, HTTPS, FTP, SSH, SMTP, POP3, IMAP, Telnet, SMB, DNS, RDP, VNC, MySQL, PostgreSQL, Redis, SNMP
        """
    )
    parser.add_argument("-t", "--target", required=True, help="Target IP or hostname")
    parser.add_argument("-p", "--ports", required=True, help="Port list (e.g., 22,80 or 1-1024 or 'all')")
    parser.add_argument("--threads", type=int, default=100, help="Number of threads (default: 100)")
    parser.add_argument("--log", default="scan_results.log", help="Log file (default: scan_results.log)")
    parser.add_argument("--show-closed", action="store_true", help="Show closed ports")
    parser.add_argument("--udp", action="store_true", help="Enable UDP scanning")
    return parser

def validate_args(args):
    if not (1 <= args.threads <= 1000):
        safe_print(f"{Fore.RED}[!] Thread count must be between 1 and 1000")
        sys.exit(1)

def show_banner():
    safe_print(f"{Fore.CYAN}{'='*60}")
    safe_print(f"{Fore.CYAN}Advanced Multi-Protocol Port Scanner v0.0.1")
    safe_print(f"{Fore.CYAN}{'='*60}")

def main():
    parser = create_parser()
    args = parser.parse_args()

    validate_args(args)

    ports = parse_ports(args.ports)
    show_closed = args.show_closed or args.ports.lower() != "all"

    show_banner()

    scanner = PortScanner(
        target=args.target,
        ports=ports,
        max_threads=args.threads,
        show_closed=show_closed,
        log_file=args.log,
        udp_mode=args.udp
    )

    try:
        scanner.run()
    except KeyboardInterrupt:
        safe_print(f"\n{Fore.YELLOW}[!] Scan interrupted by user")
        scanner.stop()
        sys.exit(0)
    except Exception as e:
        safe_print(f"{Fore.RED}[!] Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
