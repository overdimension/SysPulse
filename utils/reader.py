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
    
