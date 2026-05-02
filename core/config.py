import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, 'logs')
CSV_PATH = os.path.join(BASE_DIR, "metrics_history.csv")

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

DEFAULT_INTERVAL = 5
APP_VERSION = "0.2.0"
APP_NAME = "SysPulse"

CHART_COLORS = {
    "cpu": "#FF4B4B",
    "memory": "#0068C9",
    "disk": "#29B09D"
}