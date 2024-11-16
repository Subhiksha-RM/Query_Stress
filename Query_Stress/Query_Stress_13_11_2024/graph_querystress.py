import json
import networkx as nx
import os
import psutil
import time
from datetime import datetime, timedelta
from functools import lru_cache

@lru_cache(maxsize=None)
def load_json_file(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def load_and_build_graph(folder_path):
    graphs = []
    files_without_values = []
    parsed_files = set()

    # Load and build a directed graph from multiple JSON files in the folder
    for i, file_name in enumerate(os.listdir(folder_path)):
        if file_name.endswith('.json'):
            file_path = os.path.join(folder_path, file_name)
            graph_data = load_json_file(file_path)
            G = nx.DiGraph()
            for node in graph_data['nodes']:
                G.add_node(node['id'], **node)
            for edge in graph_data['links']:
                G.add_edge(edge['source'], edge['target'], **edge)
            graphs.append((G, file_name))
            parsed_files.add(file_name)
            print(f"Graph {i+1} built from {file_path}: Nodes={G.number_of_nodes()}, Edges={G.number_of_edges()}")

    return graphs, files_without_values, parsed_files

def sum_part_costs_by_product_family(graphs, product_family_id):
    total_costs = []
    for i, (G, file_name) in enumerate(graphs):
        total_cost = 0
        family_exists = False
        for node_id, node_data in G.nodes(data=True):
            if node_data.get('node_type') == 'Parts' and node_data.get('product_family_id') == product_family_id:
                total_cost += node_data.get('cost', 0)
                family_exists = True
        total_costs.append((file_name, i+1, total_cost))
        print(f"Product family {product_family_id} {'exists' if family_exists else 'does not exist'} in graph {i+1} (built from {file_name})")
    return total_costs

def sum_part_costs_by_product_offering(graphs, product_offering_id):
    total_costs2 = []
    for i, (G, file_name) in enumerate(graphs):
        total_cost2 = 0
        offering_exists = False
        for node_id, node_data in G.nodes(data=True):
            if node_data.get('node_type') == 'Parts' and node_data.get('product_offering_id') == product_offering_id:
                total_cost2 += node_data.get('cost', 0)
                offering_exists = True
        total_costs2.append((file_name, i+1, total_cost2))
        print(f"Product offering {product_offering_id} {'exists' if offering_exists else 'does not exist'} in graph {i+1} (built from {file_name})")
    return total_costs2

def get_part_cost_by_id(graphs, part_id):
    for i, (G, file_name) in enumerate(graphs):
        part_exists = False
        for node_id, node_data in G.nodes(data=True):
            if node_id == part_id and node_data.get('node_type') == 'Parts':
                part_exists = True
                print(f"Part {part_id} exists in graph {i+1} (built from {file_name})")
                return node_data.get('cost', 0)
        if not part_exists:
            print(f"Part {part_id} does not exist in graph {i+1} (built from {file_name})")
    return None

if __name__ == "__main__":
    # Example usage
    folder_path = '/home/rm_subhiksha/LAM_SRM/Graph_Generator/v5'
    graphs, files_without_values_initial, parsed_files = load_and_build_graph(folder_path)

    def memory_usage():
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / (1024 ** 2)  # bytes to MB conversion
    
    start_time = time.time()
    start_memory = memory_usage()

    # Sum costs for a specific product family
    product_family_id = '1-2'  # Example product family ID
    total_costs_by_family = sum_part_costs_by_product_family(graphs, product_family_id)

    # Print the cost of parts for each .json file separately with the .json file name and graph name
    for file_name, graph_index, total_cost in total_costs_by_family:
        print(f"Total cost of all parts under product family {product_family_id} in graph {graph_index} (built from {file_name}): {total_cost}")

       # Sum costs for a specific product off
    product_offering_id = '1-2-3'
    total_costs_by_offering = sum_part_costs_by_product_offering(graphs, product_offering_id)

    # Print the cost of parts for each .json file separately with the .json file name and graph name
    for file_name, graph_index, total_cost2 in total_costs_by_offering:
        print(f"Total cost of all parts under product offering {product_offering_id} in graph {graph_index} (built from {file_name}): {total_cost2}")

    # Get cost for a specific part
    part_id = '1-1-1-1-1'  # Example part ID
    part_cost = get_part_cost_by_id(graphs, part_id)
    print(f"Cost of part with ID {part_id}: {part_cost}")

    # Check if all JSON files are parsed
    all_files_parsed = set(os.listdir(folder_path)) == parsed_files

    if files_without_values_initial:
        print("Files without the required values:")
        for file_name in files_without_values_initial:
            print(file_name)

    print(f"All JSON files parsed: {all_files_parsed}")

    end_memory = memory_usage()
    end_time = time.time()
    time_taken = end_time - start_time
    memory_used = end_memory - start_memory
    print("Time taken in seconds: ", time_taken)
    print("Memory Used in MB: ", memory_used)

