from core.agent import MonitoringAgent
from utils.reader import analyze_logs
import sys

def run():
    if len(sys.argv) > 1 and sys.argv[1] == "--analyze":
        analyze_logs("logs/monitoring_agent.log")

    agent = MonitoringAgent(interval=2)
    agent.start()

if __name__ == "__main__":
    run()