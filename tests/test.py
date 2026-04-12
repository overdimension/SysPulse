from collectors.cpu import CPUCollector
from collectors.memory import MemoryCollector
from collectors.disk import DiskCollector
from collectors.processes import ProcessesCollector

from tabulate import tabulate

def run_test():
    monitors = [
        CPUCollector(),
        MemoryCollector(),
        DiskCollector(),
        ProcessesCollector()
    ]

    print("Running tests for collectors...\n")

    for m in monitors:
        result = m.get_data()
        name = result['collector'].upper()
        timestamp = result['timestamp']

        if result['status'] == 'success':
            print(f"[{timestamp}] {name} Collector: SUCCESS")

            for key, value in result['metrics'].items():
                print(f"  -> {key}: {value}")
        else:
            print(f"[{timestamp}] {name} Collector: ERROR - {result.get('message', 'Unknown error')}")

        
        if result["collector"] == "processes":
            top_processes = result['metrics']['top_processes']

            print(tabulate(top_processes, headers="keys", tablefmt="grid"))

if __name__ == "__main__":
    run_test()