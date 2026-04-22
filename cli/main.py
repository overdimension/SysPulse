import argparse
import sys
from core.agent import MonitoringAgent
from utils.reader import analyze_logs

def run():
    # Создаем парсер аргументов
    parser = argparse.ArgumentParser(
        description="Sys-Pulse: Профессиональная система мониторинга ресурсов ПК"
    )

    # Добавляем флаг для анализа
    parser.add_argument(
        "--analyze", 
        action="store_true", 
        help="Запустить анализ накопленных логов вместо мониторинга"
    )

    # Добавляем аргумент для интервала
    parser.add_argument(
        "-i", "--interval", 
        type=int, 
        default=5, 
        help="Интервал между сборами данных в секундах (по умолчанию: 5)"
    )

    args = parser.parse_args()

    # Логика выбора режима
    if args.analyze:
        # Важно: убедись, что имя файла совпадает с тем, что в настройках logging
        analyze_logs("logs/agent.log")
    else:
        print(f"🚀 Запуск мониторинга (интервал: {args.interval}с)...")
        print("Нажмите Ctrl+C для остановки.")
        
        try:
            agent = MonitoringAgent(interval=args.interval)
            agent.start()
        except KeyboardInterrupt:
            print("\n🛑 Мониторинг остановлен пользователем.")
        except Exception as e:
            print(f"💥 Критическая ошибка: {e}")

if __name__ == "__main__":
    run()