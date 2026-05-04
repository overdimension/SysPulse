import functools
import time
import asyncio
from datetime import datetime

def log(level="INFO"):
    def decorator(func):
        is_async = asyncio.is_coroutinefunction(func)

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            try:
                result = await func(*args, **kwargs)
                exec_time = time.perf_counter() - start_time
                timestamp = datetime.now().isoformat()
                print(f"[{timestamp}] {level} | {func.__name__} (async) | Success")
                return result
            except Exception as e:
                timestamp = datetime.now().isoformat()
                print(f"[{timestamp}] ERROR | {func.__name__} (async) | Exception: {e}")
                raise

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            try:
                result = func(*args, **kwargs)
                exec_time = time.perf_counter() - start_time
                timestamp = datetime.now().isoformat()
                print(f"[{timestamp}] {level} | {func.__name__} | Success")
                return result
            except Exception as e:
                timestamp = datetime.now().isoformat()
                print(f"[{timestamp}] ERROR | {func.__name__} | Exception: {e}")
                raise

        return async_wrapper if is_async else sync_wrapper

    return decorator