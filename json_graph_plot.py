import matplotlib.pyplot as plt

# Sample data for JSON querying
json_cores = [6, 8, 10, 12, 14, 16, 18, 20, 22, 24]
json_total_time = [2.846, 2.803, 2.872, 2.785, 2.772, 2.797, 2.838, 2.808, 2.816, 2.827]
# json_current_memory = []
# json_peak_memory = []
# json_cpu_usage = []
json_memory_usage = [24.3, 17.7, 17.70, 27.9, 9.1, 17.7, 38.8, 17.0, 72.2, 42.2, 43.6]

# Sample data for Graph querying (assuming similar pattern)
graph_total_time = [2.868, 2.881, 2.882, 2.898, 2.907, 2.872, 2.905, 2.900, 2.896, 2.940]
# graph_current_memory = [65, 70, 72, 75, 77, 80, 78.5, 82, 85, 87]
# graph_peak_memory = [95, 100, 105, 108, 110, 112, 110.5, 115, 118, 120]
# graph_cpu_usage = [1.4, 1.5, 1.6, 1.7, 1.75, 1.8, 1.85, 1.9, 2.0, 2.05]
graph_memory_usage = [279.4, 254.9, 238.6, 250.6, 236.4, 298.7, 226.7, 369.6, 305.8, 239.3]

# Plotting the graphs
plt.figure(figsize=(15, 10))

plt.subplot(3, 2, 1)
plt.plot(json_cores, json_total_time, label='JSON Querying')
plt.plot(json_cores, graph_total_time, label='Graph Querying')
plt.xlabel('Number of Cores')
plt.ylabel('Total Time Taken (seconds)')
plt.title('Total Time Taken vs Number of Cores')
plt.legend()

# plt.subplot(3, 2, 2)
# plt.plot(json_cores, json_current_memory, label='JSON Querying')
# plt.plot(json_cores, graph_current_memory, label='Graph Querying')
# plt.xlabel('Number of Cores')
# plt.ylabel('Current Memory Usage (MB)')
# plt.title('Current Memory Usage vs Number of Cores')
# plt.legend()

# plt.subplot(3, 2, 3)
# plt.plot(json_cores, json_peak_memory, label='JSON Querying')
# plt.plot(json_cores, graph_peak_memory, label='Graph Querying')
# plt.xlabel('Number of Cores')
# plt.ylabel('Peak Memory Usage (MB)')
# plt.title('Peak Memory Usage vs Number of Cores')
# plt.legend()

# plt.subplot(3, 2, 4)
# plt.plot(json_cores, json_cpu_usage, label='JSON Querying')
# plt.plot(json_cores, graph_cpu_usage, label='Graph Querying')
# plt.xlabel('Number of Cores')
# plt.ylabel('CPU Usage (%)')
# plt.title('CPU Usage vs Number of Cores')
# plt.legend()

plt.subplot(3, 2, 5)
plt.plot(json_cores, json_memory_usage, label='JSON Querying')
plt.plot(json_cores, graph_memory_usage, label='Graph Querying')
plt.xlabel('Number of Cores')
plt.ylabel('Memory Usage (MB)')
plt.title('Memory Usage vs Number of Cores')
plt.legend()

# Adjust layout and show plot
plt.tight_layout()
plt.show()
