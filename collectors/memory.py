import psutil

mem = psutil.virtual_memory()

GB = 1024 ** 3

def get_memory_info():
    return {
        "total": mem.total,
        "used": mem.used,
        "available": mem.available,
        "percent": mem.percent
    }