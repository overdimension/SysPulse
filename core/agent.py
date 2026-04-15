import time
from tabulate import tabulate
from collectors.cpu import CPUCollector
from collectors.memory import MemoryCollector
from collectors.disk import DiskCollector
from collectors.processes import ProcessesCollector

class MonitoringAgent:
    def __init__(self, interval=5):
        self.interval = interval
        self.collectors = [
            CPUCollector(),
            MemoryCollector(),
            DiskCollector(),
            ProcessesCollector()
        ]
        self.running = False


    """Запуск бесконечного цикла мониторинга"""
    def start(self):
        self.running = True
        print("Monitoring Agent started.")
        print("Ctrl+C to stop.")

        try:
            while self.running:
                self.process_tick()
                time.sleep(self.interval)
        except KeyboardInterrupt:
            self.stop()


    """Цикл опроса датчиков"""
    def process_tick(self):
        print(f"\n--- Collecting data at {time.strftime('%Y-%m-%d %H:%M:%S')} ---")
        for collector in self.collectors:
            data = collector.get_data()

            if data["status"] == "success":
                if data["collector"] == "processes" and "top_processes" in data["metrics"]:
                    print(f"[{data['collector'].upper()}]:")
                    print(tabulate(data["metrics"]["top_processes"], headers="keys", tablefmt="grid"))
                else:
                    metrics = data['metrics']
                    metrics_str = ", ".join([f"{key}: {value}" for key, value in metrics.items()])
                    print(f"[{data['collector'].upper()}]: {metrics_str}")
            else:
                print(f"Mistake in {data['collector']}: {data.get('message', 'Unknown error')}")

        self.analyze_process_stream()
        

    def analyze_process_stream(self):
        """Анализ потоковых данных о процессах"""
        processes_collector = next((c for c in self.collectors if isinstance(c, ProcessesCollector)), None)
        if processes_collector:
            print("\nStreaming process data (Ctrl+C to stop):")
            high_load_counter = 0

            for proc in processes_collector.stream_processes():
                if proc['cpu_percent'] > 50:
                    high_load_counter += 1
                    print(f"High CPU usage detected: {proc['name']} (PID: {proc['pid']}, CPU: {proc['cpu_percent']}%)")

                if high_load_counter == 0:
                    print("No high CPU usage detected in the last interval.")
            

    """Остановка агента"""
    def stop(self):
        self.running = False
        print("\nMonitoring Agent stopped.")