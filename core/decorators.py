import functools
import time
import asyncio
from datetime import datetime

def log(level="INFO"):
    def decorator(func):
        is_async = asyncio.is_coroutinefunction(func)

        # An additional function for logging (to avoid duplicating the code in both wrappers)
        def log_message(args, kwargs, result, exec_time, error=None):
            timestamp = datetime.now().isoformat()
            
            # REALIZATION OF FILTERING: if level is ERROR and there is no error — do not print anything
            if level == "ERROR" and error is None:
                return

            status = "Success" if error is None else f"Exception: {error}"
            suffix = "(async)" if is_async else ""
            
            print(f"[{timestamp}] {level} | {func.__name__} {suffix} | {status} | Time: {exec_time:.4f}s")

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            try:
                result = await func(*args, **kwargs)
                exec_time = time.perf_counter() - start_time
                log_message(args, kwargs, result, exec_time)
                return result
            except Exception as e:
                exec_time = time.perf_counter() - start_time
                log_message(args, kwargs, None, exec_time, error=e)
                raise

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            try:
                result = func(*args, **kwargs)
                exec_time = time.perf_counter() - start_time
                log_message(args, kwargs, result, exec_time)
                return result
            except Exception as e:
                exec_time = time.perf_counter() - start_time
                log_message(args, kwargs, None, exec_time, error=e)
                raise

        return async_wrapper if is_async else sync_wrapper
    return decorator