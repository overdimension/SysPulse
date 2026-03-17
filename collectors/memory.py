import psutil

def get_memory_info():
    mem = psutil.virtual_memory()
    GB = 1024 ** 3 

    return {
        "total": round(mem.total / GB, 2),
        "used": round(mem.used / GB, 2),
        "available": round(mem.available / GB, 2),
        "percent": mem.percent
    }
