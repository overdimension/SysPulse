import time
import logging
import os
from tabulate import tabulate
from collectors.cpu import CPUCollector
from collectors.memory import MemoryCollector
from collectors.disk import DiskCollector
from collectors.processes import ProcessesCollector
from storage.memory_storage import MemoryStorage


if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/monitoring_agent.log"),
        logging.StreamHandler()
    ]
)

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
        self.storage = MemoryStorage()


    """Запуск бесконечного цикла мониторинга"""
    def start(self):
        self.running = True
        logging.info("Monitoring Agent started.")
        logging.info("Ctrl+C to stop.")

        try:
            while self.running:
                self.process_tick()
                time.sleep(self.interval)
        except KeyboardInterrupt:
            self.stop()


    """Цикл опроса датчиков"""
    def process_tick(self):
        logging.info(f"Collecting data at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        for collector in self.collectors:
            data = collector.get_data()

            if data["status"] == "success":
                self.storage.save(data['collector'], data['metrics'])
                logging.info(f"Data for {data['collector']} saved to RAM.")
                if data["collector"] == "processes" and "top_processes" in data["metrics"]:
                    logging.info(f"[{data['collector'].upper()}]:")
                    logging.info(tabulate(data["metrics"]["top_processes"], headers="keys", tablefmt="grid"))
                else:
                    metrics = data['metrics']
                    metrics_str = ", ".join([f"{key}: {value}" for key, value in metrics.items()])
                    logging.info(f"[{data['collector'].upper()}]: {metrics_str}")
            else:
                logging.error(f"Error in {data['collector']}: {data.get('message', 'Unknown error')}")

        self.analyze_process_stream()
        

    def analyze_process_stream(self):
        """Анализ потоковых данных о процессах"""
        processes_collector = next((c for c in self.collectors if isinstance(c, ProcessesCollector)), None)
        if processes_collector:
            logging.info("\nStreaming process data (Ctrl+C to stop):")
            high_load_counter = 0

            for proc in processes_collector.stream_processes():
                if proc['cpu_percent'] > 50:
                    high_load_counter += 1
                    logging.warning(f"High CPU usage detected: {proc['name']} (PID: {proc['pid']}, CPU: {proc['cpu_percent']}%)")

                if high_load_counter == 0:
                    logging.info("No high CPU usage detected in the last interval.")
            

    """Остановка агента"""
    def stop(self):
        self.running = False
        logging.info("\nMonitoring Agent stopped.")
