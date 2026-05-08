import json
import os
from datetime import datetime
from pathlib import Path


class CloudStorage:
    """Mock cloud storage for metrics - stores data as JSON"""
    
    def __init__(self, storage_dir="cloud_data"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        self.metrics_file = self.storage_dir / "metrics.json"
        self._init_storage()
    
    def _init_storage(self):
        """Initialize storage file if it doesn't exist"""
        if not self.metrics_file.exists():
            self._write_data([])
    
    def _read_data(self):
        """Read all metrics from storage"""
        try:
            with open(self.metrics_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    
    def _write_data(self, data):
        """Write metrics to storage"""
        with open(self.metrics_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def save_metrics(self, metrics):
        """Save metrics to cloud storage"""
        data = self._read_data()
        entry = {
            "timestamp": datetime.now().isoformat(),
            "metrics": metrics
        }
        data.append(entry)
        # Keep only last 1000 entries to avoid huge files
        if len(data) > 1000:
            data = data[-1000:]
        self._write_data(data)
        return True
    
    def get_all_metrics(self):
        """Get all stored metrics"""
        return self._read_data()
    
    def get_last_metrics(self, count=10):
        """Get last N metrics"""
        data = self._read_data()
        return data[-count:] if data else []
    
    def get_metrics_by_collector(self, collector_name):
        """Get all metrics from specific collector"""
        data = self._read_data()
        return [
            entry for entry in data 
            if entry.get('metrics', {}).get('collector') == collector_name
        ]
    
    def get_statistics(self):
        """Get statistics about stored metrics"""
        data = self._read_data()
        return {
            "total_entries": len(data),
            "first_entry": data[0] if data else None,
            "last_entry": data[-1] if data else None,
            "storage_file": str(self.metrics_file)
        }
    
    def clear_all(self):
        """Clear all stored metrics"""
        self._write_data([])
        return True
