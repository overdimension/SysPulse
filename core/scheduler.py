import schedule
import time
import threading
from core.config import DEFAULT_INTERVAL

class TaskScheduler:
    def __init__(self):
        self.is_running = False

    def add_job(self, task_func, interval=DEFAULT_INTERVAL):
        """Добавляет задачу в расписание"""
        schedule.every(interval).seconds.do(task_func)
        print(f"📅 Task registered: {task_func.__name__} every {interval}s")

    def run_pending(self):
        """Запуск цикла проверки задач"""
        self.is_running = True
        while self.is_running:
            schedule.run_pending()
            time.sleep(1)

    def stop(self):
        self.is_running = False