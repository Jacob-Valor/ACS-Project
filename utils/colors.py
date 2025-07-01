"""
Color output utilities and formatting functions.
"""

from datetime import datetime
from colorama import Fore, Back, Style, init
from config.settings import UTC_PLUS_7

# Initialize colorama
init(autoreset=True)


def print_banner():
    """Print the application banner."""
    banner = f"""
{Fore.CYAN}{'='*60}
{Fore.YELLOW}    Advanced Port Scanner v0.0.1
{Fore.CYAN}    TCP/UDP Scanner with Service Detection
{Fore.GREEN}    Author: 3rd ACS Project Group 10
{Fore.CYAN}{'='*60}{Style.RESET_ALL}
"""
    print(banner)


def format_timestamp():
    """Format current timestamp with timezone."""
    return datetime.now(UTC_PLUS_7).strftime("%Y-%m-%d %H:%M:%S UTC+07:00")


def colored_status(status, port, protocol="TCP"):
    """Return colored status string."""
    timestamp = format_timestamp()
    
    if status == "OPEN":
        return f"{Fore.GREEN}[{timestamp}] [+] {protocol} Port {port} is OPEN"
    elif status == "CLOSED":
        return f"{Fore.RED}[{timestamp}] [-] {protocol} Port {port} is CLOSED"
    elif status == "FILTERED":
        return f"{Fore.MAGENTA}[{timestamp}] [?] {protocol} Port {port} is FILTERED"
    else:
        return f"{Fore.YELLOW}[{timestamp}] [!] {protocol} Port {port} - {status}"