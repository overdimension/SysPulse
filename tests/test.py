from collectors.cpu import CPUCollector
from collectors.memory import MemoryCollector

monitors = [CPUCollector(), MemoryCollector()]

print("--SysPulse System Monitor--")

for m in monitors:
    result = m.get_data()
    if result["status"] == "success":
        print(f"[{result['collector'].upper()}] Usage: {result['metrics']}")
    else:
        print(f"Error in {result['collector']}: {result['message']}")
