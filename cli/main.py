from core.agent import MonitoringAgent

def run():
    agent = MonitoringAgent(interval=2)
    agent.start()

if __name__ == "__main__":
    run()