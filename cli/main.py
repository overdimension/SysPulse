import argparse
import sys
from core.agent import MonitoringAgent
from utils.reader import analyze_logs, analyze_metrics

def run():
    # Создаем парсер аргументов
    parser = argparse.ArgumentParser(
        description="Sys-Pulse: Professional resource monitoring system"
    )

    # Добавляем флаг для анализа
    parser.add_argument(
        "--analyze", 
        action="store_true", 
        help="Run analysis of accumulated logs instead of monitoring"
    )

    # Добавляем аргумент для интервала
    parser.add_argument(
        "-i", "--interval", 
        type=int, 
        default=5, 
        help="Interval between data collections in seconds (default: 5)"
    )

    args = parser.parse_args()

    # Логика выбора режима
    if args.analyze:
        analyze_logs()
        analyze_metrics()
    else:
        print(f"🚀 Starting monitoring (interval: {args.interval}s)...")
        print("Press Ctrl+C to stop.")
        
        try:
            agent = MonitoringAgent(interval=args.interval)
            agent.start()
        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped by user.")
        except Exception as e:
            print(f"💥 Critical error: {e}")

if __name__ == "__main__":
    run()