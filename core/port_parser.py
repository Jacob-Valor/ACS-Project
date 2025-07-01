"""
Port range parsing utilities.
"""

import sys
from colorama import Fore, Style


def parse_ports(port_arg):
    """
    Parse port specification into a list of ports.
    
    Args:
        port_arg (str): Port specification (e.g., "22,80", "1-1000", "all")
        
    Returns:
        list: Sorted list of port numbers
    """
    if port_arg.lower() == "all":
        return list(range(1, 65536))  # Full port range
    
    ports = set()
    
    try:
        for part in port_arg.split(','):
            part = part.strip()
            
            if '-' in part:
                # Handle port ranges
                start, end = part.split('-', 1)
                start, end = int(start.strip()), int(end.strip())
                
                if start > end:
                    raise ValueError(f"Invalid range: {start}-{end}")
                if start < 1 or end > 65535:
                    raise ValueError(f"Port numbers must be between 1 and 65535")
                
                ports.update(range(start, end + 1))
            else:
                # Handle individual ports
                port = int(part)
                if port < 1 or port > 65535:
                    raise ValueError(f"Port number must be between 1 and 65535: {port}")
                ports.add(port)
        
        return sorted(ports)
        
    except ValueError as e:
        print(f"{Fore.RED}[!] Invalid port format: {e}{Style.RESET_ALL}")
        sys.exit(1)
        
"""
Port range parsing utilities.
"""

import sys
from colorama import Fore, Style


def parse_ports(port_arg):
    """
    Parse port specification into a list of ports.
    
    Args:s
        port_arg (str): Port specification (e.g., "22,80", "1-1000", "all")
        
    Returns:
        list: Sorted list of port numbers
    """
    if port_arg.lower() == "all":
        return list(range(1, 65536))  # Full port range
    
    ports = set()
    
    try:
        for part in port_arg.split(','):
            part = part.strip()
            
            if '-' in part:
                # Handle port ranges
                start, end = part.split('-', 1)
                start, end = int(start.strip()), int(end.strip())
                
                if start > end:
                    raise ValueError(f"Invalid range: {start}-{end}")
                if start < 1 or end > 65535:
                    raise ValueError(f"Port numbers must be between 1 and 65535")
                
                ports.update(range(start, end + 1))
            else:
                # Handle individual ports
                port = int(part)
                if port < 1 or port > 65535:
                    raise ValueError(f"Port number must be between 1 and 65535: {port}")
                ports.add(port)
        
        return sorted(ports)
        
    except ValueError as e:
        print(f"{Fore.RED}[!] Invalid port format: {e}{Style.RESET_ALL}")
        sys.exit(1)