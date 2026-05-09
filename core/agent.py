import time
import logging
import os
import sys
import asyncio
import threading
from tabulate import tabulate

from collectors.cpu import CPUCollector
from collectors.memory import MemoryCollector
from collectors.disk import DiskCollector
from collectors.processes import ProcessesCollector
from storage.memory_storage import MemoryStorage
from storage.csv_storage import CSVStorage
from core.http_client import CloudExporter, AuthProxy, BaseHttpClient, LocalCloudClient

from core.config import DEFAULT_INTERVAL, LOG_DIR, CSV_PATH, APP_VERSION
from core.scheduler import TaskScheduler
from core.decorators import log
from core.events import EventEmitter
from utils.reader import AsyncLogReader, error_filter

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
    # Event type constants
    EVENT_METRICS_COLLECTED = "metrics_collected"
    EVENT_DISPLAY_METRICS = "display_metrics"
    EVENT_HIGH_LOAD = "high_load"
    
    def __init__(self, interval=DEFAULT_INTERVAL, api_key=None):
        self.interval = interval
        self.scheduler = TaskScheduler()
        self.event_emitter = EventEmitter()
        self.log_file = os.path.join(LOG_DIR, "agent.log")
        
        self.collectors = [
            CPUCollector(),
            MemoryCollector(),
            DiskCollector(),
            ProcessesCollector()
        ]
        
        self.storages = [
            MemoryStorage(),
            CSVStorage()
        ]
        
        # Initialize cloud exporter if API key is provided
        self.cloud_exporter = None
        if api_key:
            try:
                # Use local cloud storage by default (development mode)
                local_client = LocalCloudClient()
                # Optionally wrap with auth proxy for real API
                # auth_client = AuthProxy(local_client, api_key)
                self.cloud_exporter = CloudExporter(local_client)
                logging.info("☁️ Cloud export enabled (local storage mode)")
            except Exception as e:
                logging.error(f"❌ Failed to initialize cloud exporter: {e}")
        
        # Register default storage listeners
        self._register_storage_listeners()

    @log(level="INFO")
    def start(self):
        """Start the agent via the scheduler"""
        logging.info(f"🚀 SysPulse Agent v{APP_VERSION} started.")
        logging.info("Press Ctrl+C to stop.")

        # Start async log monitoring in a separate thread
        def run_async_loop():
            asyncio.run(self.monitor_logs())
        
        thread = threading.Thread(target=run_async_loop, daemon=True)
        thread.start()

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

    @log(level="INFO")
    def process_tick(self):
        """Main data collection loop"""
        logging.info("\n" + "─"*60)
        logging.info(f"Collecting metrics | {time.strftime('%H:%M:%S')}")
        logging.info("─"*60)
        
        for collector in self.collectors:
            try:
                data = collector.get_data()
                if data["status"] == "success":
                    # Emit event instead of direct storage calls
                    self.event_emitter.emit(self.EVENT_METRICS_COLLECTED, data)
                    self.event_emitter.emit(self.EVENT_DISPLAY_METRICS, data)
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

    def _register_storage_listeners(self):
        """Register event listeners for storage operations"""
        for storage in self.storages:
            self.event_emitter.subscribe(self.EVENT_METRICS_COLLECTED, lambda data, s=storage: self._save_to_storage(s, data))
        self.event_emitter.subscribe(self.EVENT_DISPLAY_METRICS, self._display_metrics)
        self.event_emitter.subscribe(self.EVENT_HIGH_LOAD, self._on_high_load)
    
    def add_storage(self, storage):
        """Add a new storage listener to the agent"""
        self.storages.append(storage)
        self.event_emitter.subscribe(self.EVENT_METRICS_COLLECTED, lambda data, s=storage: self._save_to_storage(s, data))
    
    def _save_to_storage(self, storage, data):
        """Save metrics to a specific storage instance"""
        try:
            storage.save(data['collector'], data['metrics'])
            # Also export to cloud if exporter is available
            if self.cloud_exporter:
                self._export_to_cloud(data)
        except Exception as e:
            logging.error(f"❌ Error saving metrics to {storage.__class__.__name__}: {e}")
    
    def _export_to_cloud(self, data):
        """Export metrics to cloud"""
        try:
            result = self.cloud_exporter.export_data(data['metrics'])
            if result.get('status') == 200:
                logging.debug("✅ Metrics exported to cloud")
            else:
                logging.warning(f"⚠️ Cloud export returned status: {result.get('status')}")
        except Exception as e:
            logging.error(f"❌ Error exporting to cloud: {e}")
    
    def _on_high_load(self, proc):
        """Handle high load process event"""
        logging.warning(f"⚠️ HIGH LOAD: {proc['name']} (PID: {proc['pid']}, CPU: {proc['cpu_percent']}%)")

    async def monitor_logs(self):
        """Asynchronous log monitoring for real-time error alerts"""
        async for alert in error_filter(AsyncLogReader(self.log_file)):
            logging.warning(alert)

    @log(level="INFO")
    def analyze_process_stream(self):
        """Separate task for analyzing heavy processes"""
        proc_col = next((c for c in self.collectors if isinstance(c, ProcessesCollector)), None)
        if proc_col:
            logging.info("\n🔍 Running background stream analysis...")
            high_load_counter = 0
            for proc in proc_col.stream_processes():
                if proc['cpu_percent'] > 50:
                    self.event_emitter.emit(self.EVENT_HIGH_LOAD, proc)
                    high_load_counter += 1
            
            if high_load_counter == 0:
                logging.info("✅ System health: OK (No heavy processes)")

    @log(level="ERROR")
    def stop(self):
        """Stop the agent and clean up resources"""
        logging.info("\n" + "━"*40)
        logging.info("Cleaning up resources and saving data...")
        self.scheduler.stop()
        logging.info("The program has been successfully completed. See you there!")
        logging.info("━"*40)
        sys.exit(0)