import multiprocessing
import time

def stress_cpu(duration):
    end_time = time.time() + duration
    while time.time() < end_time:
        pass

if __name__ == "__main__":
    duration = 1000 # Duration in seconds
    num_cores = 16  # Number of CPU cores to use

    processes = []
    for _ in range(num_cores):
        p = multiprocessing.Process(target=stress_cpu, args=(duration,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
