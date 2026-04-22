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
        logging.info(f"--- Data collection cycle: {time.strftime('%H:%M:%S')} ---")
        
        for collector in self.collectors:
            try:
                data = collector.get_data()

                if data["status"] == "success":
                    self.storage.save(data['collector'], data['metrics'])
                    logging.info(f"Данные {data['collector']} успешно сохранены.")

                    if data["collector"] == "processes" and "top_processes" in data["metrics"]:
                        logging.info(f"[{data['collector'].upper()}]:\n" + 
                                     tabulate(data["metrics"]["top_processes"], headers="keys", tablefmt="grid"))
                    else:
                        metrics_str = ", ".join([f"{k}: {v}" for k, v in data['metrics'].items()])
                        logging.info(f"[{data['collector'].upper()}]: {metrics_str}")
                else:
                    logging.warning(f"⚠️ Коллектор {data['collector']} сообщил об ошибке: {data.get('message')}")

            except Exception as e:
                logging.error(f"🚨 Непредвиденная ошибка в {collector.__class__.__name__}: {str(e)}")

        # 5. Запуск потокового анализа (Large Data Processing)
        try:
            self.analyze_process_stream()
        except Exception as e:
            logging.error(f"🚨 Ошибка при потоковом анализе процессов: {e}")
        

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
