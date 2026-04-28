import csv
import logging
import os

def log_stream_reader(file_path):
    """
    Инкрементальное чтение логов без загрузки всего файла в RAM.
    """
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                yield line


def analyze_logs(log_file="logs/agent.log"):
    """Анализ ошибок, используя потоковое чтение логов"""
    count = 0
    print(f"--- Error analysis in {log_file} ---")
    
    for line in log_stream_reader(log_file):
        if "[ERROR]" in line:
            print(f"⚠ An error was found: {line.strip()}")
            count += 1
            
    print(f"✅ Total critical incidents: {count}")
    
    

def analyze_metrics(csv_file="logs/metrics_history.csv"):
    """Анализ метрик из CSV с помощью потокового чтения"""
    if not os.path.exists(csv_file):
        print(f"📊 Data in {csv_file} not available yet.")
        return

    stats = {}
    print(f"\n--- Statistics from {csv_file} ---")
    
    with open(csv_file, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = f"{row['collector']}_{row['metric']}"
            if key not in stats:
                stats[key] = []
            stats[key].append(float(row['value']))
    if not stats:
        print("📉 There is no data for analysis yet.")
        return

    for key, values in stats.items():
        avg_value = sum(values) / len(values)
        max_value = max(values)

        display_name = key.replace('_', ' ').title()

        print(f"🔹 {display_name}:")
        print(f"   Average: {avg_value:.2f}% | Peak: {max_value:.2f}%")