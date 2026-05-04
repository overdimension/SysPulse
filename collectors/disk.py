import psutil
from collectors.base import BaseCollector
from core.decorators import log

class DiskCollector(BaseCollector):
    @log(level="INFO")
    def collect(self) -> dict:
        usage = psutil.disk_usage('/')
        GB = 1024 ** 3

        return {
            "total_gb": round(usage.total / GB, 2),
            "used_gb": round(usage.used / GB, 2),
            "free_gb": round(usage.free / GB, 2),
            "percent_used": usage.percent
        }