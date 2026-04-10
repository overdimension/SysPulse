import psutil
from collectors.base import BaseCollector

class MemoryCollector(BaseCollector):
    def collect(self) -> dict:
        mem = psutil.virtual_memory()
        GB = 1024 ** 3

        return {
            "total_gb": round(mem.total / GB, 2),
            "available_gb": round(mem.available / GB, 2),
            "used_gb": round(mem.used / GB, 2),
            "free_gb": round(mem.free / GB, 2),
            "percent_used": mem.percent
        }