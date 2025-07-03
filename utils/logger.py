"""
Logging functionality
"""

from threading import Event
from queue import Queue, Empty

class LogManager:
    """Thread-safe logging manager"""
    
    def __init__(self, log_file):
        self.log_file = log_file
        self.log_queue = Queue()
        self.stop_event = Event()
    
    def log_message(self, message):
        """Add message to log queue"""
        try:
            self.log_queue.put_nowait(message)
        except:
            pass
    
    def log_writer(self):
        """Background thread for writing logs"""
        with open(self.log_file, "a") as f:
            while not self.stop_event.is_set():
                try:
                    msg = self.log_queue.get(timeout=1)
                    if msg:
                        f.write(msg + "\n")
                        f.flush()
                    self.log_queue.task_done()
                except Empty:
                    continue
                except Exception:
                    continue
    
    def stop(self):
        """Stop the logger"""
        self.stop_event.set()
        self.log_queue.put(None)