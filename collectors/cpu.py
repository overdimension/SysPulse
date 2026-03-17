import psutil

cpu_percent = psutil.cpu_percent(interval=1)

cpu_cores = psutil.cpu_count(logical=False)

cpu_freq = psutil.cpu_freq().current

def get_cpu_info():
    return {
        "cpu_percent": cpu_percent,
        "cpu_cores": cpu_cores,
        "cpu_freq": cpu_freq
    }