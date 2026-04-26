import csv
import os
import time
from storage.base import BaseStorage

class CSVStorage(BaseStorage):
    def __init__(self, filename="logs/metrics_history.csv"):
        self.filename = filename
        self._prepare_file()


    def _prepare_file(self):
        """Создает файл с заголовками, если его еще нет"""
        if not os.path.exists(self.filename):
            with open(self.filename, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'collector', 'metric', 'value'])


    def save(self, collector_name, metrics):
        """Записывает метрики в CSV строку за строкой"""
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        with open(self.filename, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for name, value in metrics.items():
                if isinstance(value, (int, float)):
                    writer.writerow([timestamp, collector_name, name, value])


    def get_all(self):
        """Возвращает все записанные метрики из CSV"""
        if not os.path.exists(self.filename):
            return []
        
        results = []
        with open(self.filename, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                results.append(row)
        return results


    def get_all(self, collector_name=None):
        """Возвращает все записанные метрики из CSV"""
        data = []
        try:
            with open(self.filename, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if collector_name is None or row['collector'] == collector_name:
                        data.append(row)
        except FileNotFoundError:
            return []
        return data