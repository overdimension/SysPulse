import csv
import logging

def log_stream_reader(file_path):
    """
    Инкрементальное чтение логов без загрузки всего файла в RAM.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                yield line.strip()
    except FileNotFoundError:
        yield "Log file not found."


def analyze_logs(file_path):
    """Пример обработки стрима данных"""
    print(f"--- Анализ файла {file_path} ---")
    error_count = 0

    for entry in log_stream_reader(file_path):
        if "[ERROR]" in entry or "[WARNING]" in entry:
            print(f"Found incident: {entry}")
            error_count += 1
        print(f"Total incidents found: {error_count}")
    

def get_average_cpu_usage(filename = "logs/metrics_history.csv"):
    """Анализ CSV с метриками для получения средней загрузки CPU"""
    cpu_values = []
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['collector'] == 'cpu' and row['metric'] == 'usage_percent':
                    cpu_values.append(float(row['value']))
        
        if cpu_values:
            avg = sum(cpu_values) / len(cpu_values)
            return round(avg, 2)
        return 0
    except FileNotFoundError:
        return None