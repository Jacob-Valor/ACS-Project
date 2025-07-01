"""
Configuration settings and constants for the port scanner.
"""

from datetime import timezone, timedelta

# Timezone configuration
UTC_PLUS_7 = timezone(timedelta(hours=7))

# Scanning defaults
DEFAULT_TIMEOUT = 0.5
DEFAULT_UDP_TIMEOUT = 1.0
DEFAULT_THREADS = 100
DEFAULT_LOG_FILE = "scan_results.log"

# Buffer sizes
RECV_BUFFER_SIZE = 1024
UDP_SEND_DATA = b'\x00'

# Service detection
MAX_BANNER_LENGTH = 1024
BANNER_TIMEOUT = 1.0