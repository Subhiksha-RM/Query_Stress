import multiprocessing
import time
import psutil
import json
import signal
import sys

def stress_cpu(duration):
    end_time = time.time() + duration
    while time.time() < end_time:
        pass

def log_performance(duration, interval=1):
    end_time = time.time() + duration
    performance_log = []
    while time.time() < end_time:
        cpu_usage = psutil.cpu_percent(interval=interval, percpu=True)
        memory_info = psutil.virtual_memory()
        disk_io = psutil.disk_io_counters()
        net_io = psutil.net_io_counters()
        
        log_entry = {
            "time": time.time(),
            "cpu_usage": cpu_usage,
            "memory_info": memory_info._asdict(),
            "disk_io": disk_io._asdict(),
            "net_io": net_io._asdict()
        }
        performance_log.append(log_entry)
        print(f"CPU Usage: {cpu_usage}, Memory: {memory_info.percent}%, Disk I/O: {disk_io}, Network I/O: {net_io}")
    return performance_log

def signal_handler(sig, frame):
    print('Stopping the stress test...')
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)  # Handle Ctrl+C to stop the script

    duration = 100  # Duration in seconds
    num_cores = 24   # Number of CPU cores to use

    # Start CPU stress test
    processes = []
    for _ in range(num_cores):
        p = multiprocessing.Process(target=stress_cpu, args=(duration,))
        processes.append(p)
        p.start()

    # Log performance metrics
    performance_log = log_performance(duration)

    for p in processes:
        p.join()

    # Save performance log to a file
    with open('performance_log.json', 'w') as f:
        json.dump(performance_log, f)
