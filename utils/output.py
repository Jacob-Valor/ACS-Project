"""
Output formatting and thread-safe printing
"""

from threading import Lock

print_lock = Lock()

def safe_print(message):
    """Thread-safe printing"""
    with print_lock:
        print(message)