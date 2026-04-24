import psutil
from collectors.base import BaseCollector

class ProcessesCollector(BaseCollector):
    def __init__(self):
        super().__init__()
        self.cpu_count = psutil.cpu_count() or 1

    def collect(self) -> dict:
        processes = []

        for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
            try:
                info = proc.info
                info['cpu_percent'] = round(info['cpu_percent'] / self.cpu_count, 1)
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        top_processes = sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:5]

        return {
            "top_processes": top_processes
        }

    def stream_processes(self):
        """Генератор для потоковой передачи данных о процессах"""
        for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
            try:
                info = proc.info
                info['cpu_percent'] = round(info['cpu_percent'] / self.cpu_count, 1)
                yield info
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue