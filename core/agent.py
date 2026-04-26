import time
import logging
import os
from tabulate import tabulate
from collectors.cpu import CPUCollector
from collectors.memory import MemoryCollector
from collectors.disk import DiskCollector
from collectors.processes import ProcessesCollector
from storage.memory_storage import MemoryStorage
from storage.csv_storage import CSVStorage


if not os.path.exists('logs'):
    os.makedirs('logs')

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# Настройка для ФАЙЛА 
file_handler = logging.FileHandler("logs/agent.log", encoding='utf-8')
file_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
file_handler.setLevel(logging.INFO)

# Настройка для КОНСОЛИ 
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(message)s')) # ПУСТОЙ ФОРМАТ
console_handler.setLevel(logging.INFO)

# Инициализация
logging.basicConfig(level=logging.INFO, handlers=[file_handler, console_handler])

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
        self.memory_storage = MemoryStorage()
        self.csv_storage = CSVStorage()
        self._prepare_environment()


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
            logging.info("\n" + "━"*40)
            logging.info("Stopping agent on user signal...")
        except Exception as e:
            logging.error(f"Critical failure in monitoring cycle: {e}")
        finally:
            self._cleanup()


    """Цикл опроса датчиков"""
    def process_tick(self):
        logging.info("\n" + "─"*60)
        logging.info(f"Collecting metrics | {time.strftime('%H:%M:%S')}")
        logging.info("─"*60)
        
        for collector in self.collectors:
            try:
                data = collector.get_data()
                if data["status"] == "success":
                    self.memory_storage.save(data['collector'], data['metrics'])
                    self.csv_storage.save(data['collector'], data['metrics'])
                    
                    if data["collector"] == "processes":
                        logging.info(f"\nTop processes(CPU %):")
                        table = tabulate(data["metrics"]["top_processes"], headers="keys", tablefmt="simple")
                        logging.info(table)
                    else:
                        name = data['collector'].upper()
                        m = data['metrics']
                        if name == "CPU":
                            msg = f"LOAD: {m['usage_percent']}% | CORES: {m['logical_cores']} | FREQ: {m['current_freq_mhz']} MHz"
                        elif name == "MEMORY":
                            msg = f"USED: {m['used_gb']}GB / {m['total_gb']}GB ({m['percent_used']}%)"
                        elif name == "DISK":
                            msg = f"FREE: {m['free_gb']}GB / {m['total_gb']}GB"
                        
                        logging.info(f"🔹 {name:<10} | {msg}")
            except Exception as e:
                logging.error(f"❌ Ошибка [{collector.__class__.__name__}]: {e}")
        

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


    def _prepare_environment(self):
        """Проверка и создание необходимых папок перед стартом"""
        if not os.path.exists('logs'):
            try:
                os.makedirs('logs')
                print("The 'logs' folder is created automatically.")
            except Exception as e:
                print(f"Failed to create log folder: {e}")        


    def _cleanup(self):
        """Очистка ресурсов перед выходом"""
        logging.info("Cleaning up resources and saving data...")
        logging.info("The program has been successfully completed. See you there!")
        logging.info("━"*40)


    def stop(self):
        """Остановка агента"""
        self.running = False
        logging.info("\nMonitoring Agent stopped.")

    
