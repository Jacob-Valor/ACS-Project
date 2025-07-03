#!/usr/bin/env python3
"""
Advanced Port Scanner - Entry Point
"""

import sys
import argparse
from colorama import Fore, Style

from core.scanner import PortScanner
from core.port_parser import parse_ports
from utils.colors import print_banner


def create_argument_parser():
    """Create and configure argument parser."""
    parser = argparse.ArgumentParser(
        description="Advanced TCP/UDP Port Scanner with Service Detection",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py -t 192.168.1.1 -p 22,80,443
  python main.py -t example.com -p 1-1000 --threads 200
  python main.py -t 10.0.0.1 -p all --udp --show-closed
        """
    )
    
    parser.add_argument("-t", "--target", required=True, 
                       help="Target IP address or hostname")
    parser.add_argument("-p", "--ports", required=True, 
                       help="Port specification (e.g., 22,80 or 1-1024 or 'all')")
    parser.add_argument("--threads", type=int, default=100, 
                       help="Number of concurrent threads (default: 100)")
    parser.add_argument("--log", default="scan_results.log", 
                       help="Log file path (default: scan_results.log)")
    parser.add_argument("--show-closed", action="store_true", 
                       help="Display closed/filtered ports")
    parser.add_argument("--udp", action="store_true", 
                       help="Enable UDP scanning (default: TCP)")
    parser.add_argument("--timeout", type=float, default=0.5,
                       help="Socket timeout in seconds (default: 0.5)")
    
    return parser


def main():
    """Main entry point."""
    try:
        print_banner()
        
        parser = create_argument_parser()
        args = parser.parse_args()
        
        # Parse port specification
        ports = parse_ports(args.ports)
        
        # Determine whether to show closed ports
        show_closed = args.show_closed or (args.ports.lower() != "all")
        
        # Initialize and run scanner
        scanner = PortScanner(
            target=args.target,
            ports=ports,
            max_threads=args.threads,
            show_closed=show_closed,
            log_file=args.log,
            udp_mode=args.udp,
            timeout=args.timeout
        )
        
        scanner.run()
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Scan interrupted by user.{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}[!] Fatal error: {e}{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == "__main__":
    main()