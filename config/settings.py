"""
Application settings and constants
"""

from datetime import timezone, timedelta

# Timezone configuration
UTC_PLUS_7 = timezone(timedelta(hours=7))

# Default values
DEFAULT_TIMEOUT = 0.5
MAX_THREADS = 1000
DEFAULT_LOG_FILE = "scan_results.log"

# Application information
APP_NAME = "Advanced Multi-Protocol Port Scanner"
APP_VERSION = "0.0.1"