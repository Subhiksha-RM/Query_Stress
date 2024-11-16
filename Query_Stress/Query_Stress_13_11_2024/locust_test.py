from locust import HttpUser, TaskSet, task, between, events
import os
import json
import networkx as nx
from functools import lru_cache
import time
import psutil

def memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 ** 2)  # bytes to MB conversion

class GraphQueryTasks(TaskSet):
    @task
    def query_graph(self):
        folder_path = '/home/rm_subhiksha/LAM_SRM/Graph_Generator/v5'
        graphs, files_without_values, parsed_files = self.load_and_build_graph(folder_path)
        result, files_without_values_final = self.find_best_product_offering(graphs)

        # Check if all JSON files are parsed
        all_files_parsed = set(os.listdir(folder_path)) == parsed_files

        if result:
            print(f"Best Product Offering Overall: Name={result[0]}, ID={result[1]}, Cost={result[2]}, Demand={result[3]}")
        else:
            print("No product offering found.")

        if files_without_values_final:
            print("Files without the required values:")
            for file_name in files_without_values_final:
                print(file_name)

        print(f"All JSON files parsed: {all_files_parsed}")

    @lru_cache(maxsize=None)
    def load_json_file(self, file_path):
        with open(file_path, 'r') as f:
            return json.load(f)

    def load_and_build_graph(self, folder_path):
        graphs = []
        files_without_values = []
        parsed_files = set()

        # Load and build a directed graph from multiple JSON files in the folder
        for i, file_name in enumerate(os.listdir(folder_path)):
            if file_name.endswith('.json'):


                file_path = os.path.join(folder_path, file_name)
                graph_data = self.load_json_file(file_path)
                G = nx.DiGraph()
                for node in graph_data['nodes']:
                    G.add_node(node['id'], **node)
                for edge in graph_data['links']:
                    G.add_edge(edge['source'], edge['target'], **edge)
                graphs.append((G, file_path))
                parsed_files.add(file_name)

                # end_memory = memory_usage()
                # end_time = time.time()
                # time_taken = end_time - start_time
                # memory_used = end_memory - start_memory

                print(f"Graph {i+1} built from {file_path}: Nodes={G.number_of_nodes()}, Edges={G.number_of_edges()}")
                # print("Time taken in seconds to build graph: ", time_taken)
                # print("Memory Used in MB to build graph: ", memory_used)

        return graphs, files_without_values, parsed_files

    def find_best_product_offering(self, graphs):
        best_product_offering = None
        max_demand = 0
        files_without_values = []

        # Iterate through each graph to find the product offering with max demand
        for i, (G, file_path) in enumerate(graphs):

            local_best_product_offering = None
            local_max_demand = 0
            for node_id, node_data in G.nodes(data=True):
                if node_data.get('node_type') == 'ProductOffering' and node_data.get('demand', 0) > local_max_demand:
                    local_max_demand = node_data['demand']
                    local_best_product_offering = (node_data['name'], node_id, node_data['cost'], node_data['demand'])
            
            # Display the result for the current graph
            if local_best_product_offering:
                print(f"Best Product Offering in graph {i+1} (built from {file_path}): Name={local_best_product_offering[0]}, ID={local_best_product_offering[1]}, Cost={local_best_product_offering[2]}, Demand={local_best_product_offering[3]}")
            else:
                print(f"Product offering with max demand does not exist in graph {i+1} (built from {file_path})")
                files_without_values.append(file_path)

            # Update the overall best product offering if the local one is better
            if local_max_demand > max_demand:
                max_demand = local_max_demand
                best_product_offering = local_best_product_offering

        return best_product_offering, files_without_values

class GraphQueryUser(HttpUser):
    tasks = [GraphQueryTasks]
    wait_time = between(1, 5)

if __name__ == "__main__":
    import os
    start_time = time.time()
    start_memory = memory_usage()

    os.system("locust -f locust_test.py")
    
    end_memory = memory_usage()
    end_time = time.time()
    time_taken = end_time - start_time
    memory_used = end_memory - start_memory

    print("Time taken in seconds to query graph: ", time_taken)
    print("Memory Used in MB to query graph: ", memory_used)