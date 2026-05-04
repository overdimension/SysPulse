import time
import logging
import os
import sys
from tabulate import tabulate

from collectors.cpu import CPUCollector
from collectors.memory import MemoryCollector
from collectors.disk import DiskCollector
from collectors.processes import ProcessesCollector
from storage.memory_storage import MemoryStorage
from storage.csv_storage import CSVStorage

from core.config import DEFAULT_INTERVAL, LOG_DIR, CSV_PATH, APP_VERSION
from core.scheduler import TaskScheduler

#Logging settings
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

file_handler = logging.FileHandler(os.path.join(LOG_DIR, "agent.log"), encoding='utf-8')
file_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
file_handler.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(message)s'))
console_handler.setLevel(logging.INFO)

logging.basicConfig(level=logging.INFO, handlers=[file_handler, console_handler])

class MonitoringAgent:
    def __init__(self, interval=DEFAULT_INTERVAL):
        self.interval = interval
        self.scheduler = TaskScheduler()
        
        self.collectors = [
            CPUCollector(),
            MemoryCollector(),
            DiskCollector(),
            ProcessesCollector()
        ]
        
        self.memory_storage = MemoryStorage()
        self.csv_storage = CSVStorage()

    def start(self):
        """Start the agent via the scheduler"""
        logging.info(f"🚀 SysPulse Agent v{APP_VERSION} started.")
        logging.info("Press Ctrl+C to stop.")

        #Poll all sensors
        self.scheduler.add_job(self.process_tick, self.interval)
        
        #Deep process analysis
        self.scheduler.add_job(self.analyze_process_stream, 30)

        try:
            self.scheduler.run_pending()
        except KeyboardInterrupt:
            self.stop()
        except Exception as e:
            logging.error(f"💥 Critical error: {e}")
            self.stop()

    def process_tick(self):
        """Main data collection loop"""
        logging.info("\n" + "─"*60)
        logging.info(f"Collecting metrics | {time.strftime('%H:%M:%S')}")
        logging.info("─"*60)
        
        for collector in self.collectors:
            try:
                data = collector.get_data()
                if data["status"] == "success":
                    self.memory_storage.save(data['collector'], data['metrics'])
                    self.csv_storage.save(data['collector'], data['metrics'])
                    self._display_metrics(data)
            except Exception as e:
                logging.error(f"❌ Error in [{collector.__class__.__name__}]: {e}")

    def _display_metrics(self, data):
        """Beautiful display of metrics in log/console"""
        name = data['collector'].upper()
        m = data['metrics']

        if name == "PROCESSES":
            logging.info(f"\nTop processes (CPU %):")
            table = tabulate(m["top_processes"], headers="keys", tablefmt="simple")
            logging.info(table)
        elif name == "CPU":
            logging.info(f"🔹 {name:<10} | LOAD: {m['usage_percent']}% | FREQ: {m['current_freq_mhz']} MHz")
        elif name == "MEMORY":
            logging.info(f"🔹 {name:<10} | USED: {m['used_gb']}GB / {m['total_gb']}GB ({m['percent_used']}%)")
        elif name == "DISK":
            logging.info(f"🔹 {name:<10} | FREE: {m['free_gb']}GB / {m['total_gb']}GB")

    def analyze_process_stream(self):
        """Separate task for analyzing heavy processes"""
        proc_col = next((c for c in self.collectors if isinstance(c, ProcessesCollector)), None)
        if proc_col:
            logging.info("\n🔍 Running background stream analysis...")
            high_load_counter = 0
            for proc in proc_col.stream_processes():
                if proc['cpu_percent'] > 50:
                    logging.warning(f"⚠️ HIGH LOAD: {proc['name']} (PID: {proc['pid']}, CPU: {proc['cpu_percent']}%)")
                    high_load_counter += 1
            
            if high_load_counter == 0:
                logging.info("✅ System health: OK (No heavy processes)")

    def stop(self):
        """Stop the agent and clean up resources"""
        logging.info("\n" + "━"*40)
        logging.info("Cleaning up resources and saving data...")
        self.scheduler.stop()
        logging.info("The program has been successfully completed. See you there!")
        logging.info("━"*40)
        sys.exit(0)