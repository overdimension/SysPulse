"""
CLI tool to view and manage cloud storage metrics
"""
import argparse
import json
from tabulate import tabulate
from storage.cloud_storage import CloudStorage


def view_metrics():
    """View recent metrics from cloud storage"""
    storage = CloudStorage()
    metrics = storage.get_last_metrics(20)
    
    if not metrics:
        print("❌ No metrics found in cloud storage")
        return
    
    print(f"\n[*] Last 20 metrics from cloud storage:\n")
    
    for i, entry in enumerate(metrics, 1):
        timestamp = entry.get('timestamp', 'N/A')
        data = entry.get('metrics', {})
        
        #Try to determine collector from data structure
        collector = 'Unknown'
        if 'usage_percent' in data and 'logical_cores' in data:
            collector = 'CPU'
        elif 'total_gb' in data and 'available_gb' in data and 'used_gb' in data:
            collector = 'MEMORY'
        elif 'total_gb' in data and 'used_gb' in data and 'free_gb' in data and 'available_gb' not in data:
            collector = 'DISK'
        elif 'top_processes' in data:
            collector = 'PROCESSES'
        
        print(f"\n{i}. [{timestamp}] {collector}")
        print(f"   Data: {json.dumps(data, indent=2)}")


def view_statistics():
    """View statistics about cloud storage"""
    storage = CloudStorage()
    stats = storage.get_statistics()
    
    print(f"\n[*] Cloud Storage Statistics:\n")
    print(f"Total entries: {stats['total_entries']}")
    print(f"Storage file: {stats['storage_file']}")
    
    if stats['first_entry']:
        print(f"First entry: {stats['first_entry']['timestamp']}")
    if stats['last_entry']:
        print(f"Last entry: {stats['last_entry']['timestamp']}")


def view_by_collector(collector_name):
    """View metrics from specific collector"""
    storage = CloudStorage()
    all_metrics = storage.get_all_metrics()
    
    #Filter by collector type based on data structure
    filtered_metrics = []
    for entry in all_metrics:
        data = entry.get('metrics', {})
        entry_collector = 'Unknown'
        
        if 'usage_percent' in data and 'logical_cores' in data:
            entry_collector = 'cpu'
        elif 'total_gb' in data and 'available_gb' in data and 'used_gb' in data:
            entry_collector = 'memory'
        elif 'total_gb' in data and 'used_gb' in data and 'free_gb' in data and 'available_gb' not in data:
            entry_collector = 'disk'
        elif 'top_processes' in data:
            entry_collector = 'processes'
        
        if entry_collector.lower() == collector_name.lower():
            filtered_metrics.append(entry)
    
    if not filtered_metrics:
        print(f"❌ No metrics found for collector: {collector_name}")
        return
    
    print(f"\n📊 Metrics for {collector_name.upper()} (last {len(filtered_metrics)} entries):\n")
    
    for entry in filtered_metrics[-10:]:  #Show last 10
        timestamp = entry.get('timestamp', 'N/A')
        data = entry.get('metrics', {})
        print(f"[{timestamp}]")
        print(f"  {json.dumps(data, indent=2)}")


def clear_storage():
    """Clear all metrics from cloud storage"""
    storage = CloudStorage()
    response = input("Are you sure? This will delete all metrics (y/N): ")
    if response.lower() == 'y':
        storage.clear_all()
        print("✅ Cloud storage cleared")
    else:
        print("❌ Cancelled")


def export_to_file(filename):
    """Export all metrics to JSON file"""
    storage = CloudStorage()
    metrics = storage.get_all_metrics()
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Exported {len(metrics)} entries to {filename}")


def main():
    parser = argparse.ArgumentParser(
        description="Manage SysPulse Cloud Storage"
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # View command
    subparsers.add_parser('view', help='View recent metrics')
    
    # Stats command
    subparsers.add_parser('stats', help='View storage statistics')
    
    # View by collector
    collector_parser = subparsers.add_parser('collector', help='View metrics by collector')
    collector_parser.add_argument('name', help='Collector name (cpu, memory, disk, processes)')
    
    # Clear command
    subparsers.add_parser('clear', help='Clear all metrics')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export metrics to JSON file')
    export_parser.add_argument('filename', help='Output filename')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == 'view':
        view_metrics()
    elif args.command == 'stats':
        view_statistics()
    elif args.command == 'collector':
        view_by_collector(args.name)
    elif args.command == 'clear':
        clear_storage()
    elif args.command == 'export':
        export_to_file(args.filename)


if __name__ == '__main__':
    main()
