import psutil
from collectors.base import BaseCollector

class CPUCollector(BaseCollector):
    def collect(self) -> dict:
        return {
            "usage_percent": psutil.cpu_percent(interval=1),
            "logical_cores": psutil.cpu_count(logical=True),
            "physical_cores": psutil.cpu_count(logical=False),
            "current_freq_mhz": round(psutil.cpu_freq().current, 2) if psutil.cpu_freq() else "N/A"
        }
