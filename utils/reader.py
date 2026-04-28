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

    cpu_data = []
    mem_data = []
    print(f"\n--- Statistics from {csv_file} ---")
    
    with open(csv_file, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            val = float(row['value'])
            if row['collector'] == 'cpu' and row['metric'] == 'usage_percent':
                cpu_data.append(val)
            elif row['collector'] == 'memory' and row['metric'] == 'percent_used':
                mem_data.append(val)
    if cpu_data:
        avg_cpu = sum(cpu_data) / len(cpu_data)
        max_cpu = max(cpu_data)
        print(f"📈 Average CPU load: {avg_cpu:.2f}%")
        print(f"🔥 Maximum CPU Peak: {max_cpu:.2f}%")
        if max_cpu > 90:
            print("❗ Warning: Critical processor overloads detected!")

    elif mem_data:
        avg_mem = sum(mem_data) / len(mem_data)
        max_mem = max(mem_data)
        print(f"📊 Average Memory usage: {avg_mem:.2f}%")
        print(f"💾 Maximum Memory usage: {max_mem:.2f}%")
        if max_mem > 90:
            print("⚠ Warning: Memory usage is critically high!")
    else:
        print("📉 There is not enough data to calculate CPU yet.")