import psutil
from collectors.base import BaseCollector

class ProcessesCollector(BaseCollector):
    def collect(self) -> dict:
        processes = []

        for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        top_processes = sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:5]

        return {
            "top_processes": top_processes
        }