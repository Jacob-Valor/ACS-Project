"""
Port parsing utilities
"""

import sys
from colorama import Fore
from .output import safe_print

def parse_ports(port_arg):
    """Parse port argument into list of ports"""
    if port_arg.lower() == "all":
        return range(1, 65536)
    
    ports = set()
    try:
        for part in port_arg.split(','):
            if '-' in part:
                start, end = map(int, part.split('-'))
                ports.update(range(start, end + 1))
            else:
                ports.add(int(part.strip()))
        return sorted(ports)
    except ValueError:
        safe_print(f"{Fore.RED}[!] Invalid port format")
        sys.exit(1)