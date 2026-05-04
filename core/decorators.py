import functools
import time
from datetime import datetime

def log(level="INFO"):
    def decorator(func):
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            try:
                result = func(*args, **kwargs)
                exec_time = time.perf_counter() - start_time
                timestamp = datetime.now().isoformat()
                print(f"[{timestamp}] {level} | {func.__name__} | Success | Time: {exec_time:.4f}s")
                return result
            except Exception as e:
                timestamp = datetime.now().isoformat()
                print(f"[{timestamp}] ERROR | {func.__name__} | Exception: {e}")
                raise
        return sync_wrapper
    return decorator