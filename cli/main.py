import argparse
import sys
import os
import subprocess
from core.agent import MonitoringAgent
from utils.reader import analyze_logs, analyze_metrics, get_top_heavy_processes

def run():
    # Creating an argument parser
    parser = argparse.ArgumentParser(
        description="Sys-Pulse: Professional resource monitoring system"
    )

    # Adding argument for analysis
    parser.add_argument(
        "--analyze", 
        action="store_true", 
        help="Run analysis of accumulated logs instead of monitoring"
    )

    # Adding argument for interval
    parser.add_argument(
        "-i", "--interval", 
        type=int, 
        default=5, 
        help="Interval between data collections in seconds (default: 5)"
    )

    # Adding argument for web interface
    parser.add_argument(
        "--ui",
        action="store_true",
        help="Run the web dashboard (Streamlit)"
    )

    # Adding argument for API key (cloud export)
    parser.add_argument(
        "--api-key",
        type=str,
        default=None,
        help="API key for cloud export (or set SYSPULSE_API_KEY environment variable)"
    )

    args = parser.parse_args()

    # Logic for selecting mode
    if args.ui:
        print("🌐 Starting web dashboard...")
        current_dir = os.path.dirname(os.path.abspath(__file__))
        dash_path = os.path.normpath(os.path.join(current_dir, "..", "web", "dash.py"))
        try:
            subprocess.run([sys.executable, "-m", "streamlit", "run", dash_path])
        except KeyboardInterrupt:
            print("\n🛑 Web dashboard stopped by user.")
        
        sys.exit(0)

    elif args.analyze:
        analyze_logs()
        analyze_metrics()
        get_top_heavy_processes()

    else:
        print(f"🚀 Starting monitoring (interval: {args.interval}s)...")
        print("Press Ctrl+C to stop.")
        
        # Use API key from argument or environment variable
        api_key = args.api_key or os.getenv('SYSPULSE_API_KEY')
        
        try:
            agent = MonitoringAgent(interval=args.interval, api_key=api_key)
            agent.start()
        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped by user.")
        except Exception as e:
            print(f"💥 Critical error: {e}")

if __name__ == "__main__":
    run()