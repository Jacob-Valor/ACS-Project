"""
Logging functionality for the port scanner.
"""

import threading
from queue import Queue, Empty
from datetime import datetime
from config.settings import UTC_PLUS_7


class Logger:
    """Thread-safe logger for scan results."""
    
    def __init__(self, log_file):
        self.log_file = log_file
        self.log_queue = Queue()
        self.stop_event = threading.Event()
    
    def log(self, message):
        """Add a message to the log queue."""
        try:
            self.log_queue.put_nowait(message)
        except:
            pass  # Queue full, skip this message
    
    def writer_loop(self):
        """Main logging loop - runs in separate thread."""
        with open(self.log_file, "a", encoding='utf-8') as f:
            while not self.stop_event.is_set():
                try:
                    message = self.log_queue.get(timeout=1)
                    if message:
                        f.write(message + "\n")
                        f.flush()
                    self.log_queue.task_done()
                except Empty:
                    continue
                except Exception:
                    break
    
    def stop(self):
        """Signal the logger to stop."""
        self.stop_event.set()
        # Add a sentinel to wake up the writer thread
        try:
            self.log_queue.put_nowait(None)
        except:
            pass