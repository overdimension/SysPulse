import argparse
import sys
import os
import subprocess
from core.agent import MonitoringAgent
from utils.reader import analyze_logs, analyze_metrics, get_top_heavy_processes

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

    # Добавляем флаг для запуска веб-интерфейса
    parser.add_argument(
        "--ui",
        action="store_true",
        help="Run the web dashboard (Streamlit)"
    )

    args = parser.parse_args()

    # Логика выбора режима
    if args.analyze:
        analyze_logs()
        analyze_metrics()
        get_top_heavy_processes()
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

    if args.ui:
        print("🌐 Starting web dashboard...")
        current_dir = os.path.dirname(os.path.abspath(__file__))
        dash_path = os.path.join(current_dir, "..", "web", "dash.py")
        try:
            subprocess.run(["streamlit", "run", dash_path])
        except KeyboardInterrupt:
            print("\n🛑 Web dashboard stopped by user.")
        except FileNotFoundError:
            print("💥 Streamlit is not installed. Please install it with 'pip install streamlit' and try again.")
        return
        
if __name__ == "__main__":
    run()