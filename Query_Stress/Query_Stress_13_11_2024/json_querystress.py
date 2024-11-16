import json
import os
import psutil
from functools import lru_cache
import time
from datetime import datetime, timedelta

class JSONQuery:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    @lru_cache(maxsize=None)
    def load_json_file(self, file_path):
        with open(file_path, 'r') as f:
            return json.load(f)

    def sum_part_costs_by_product_family_prefix(self, product_family_id):
        total_costs = []
        for i, file_name in enumerate(os.listdir(self.folder_path)):
            if file_name.endswith('.json'):
                file_path = os.path.join(self.folder_path, file_name)
                data = self.load_json_file(file_path)
                total_cost = 0
                family_exists = False
                for node in data['nodes']:
                    if node.get('node_type') == 'Parts' and node['id'].startswith(product_family_id):
                        total_cost += node.get('cost', 0)
                        family_exists = True
                total_costs.append((file_name, i+1, total_cost))
                print(f"Product family {product_family_id} {'exists' if family_exists else 'does not exist'} in json {i+1} (from {file_name})")
        return total_costs
    
    def sum_part_costs_by_product_offering_prefix(self, product_offering_id):
        total_costs2 = []
        for i, file_name in enumerate(os.listdir(self.folder_path)):
            if file_name.endswith('.json'):
                file_path = os.path.join(self.folder_path, file_name)
                data = self.load_json_file(file_path)
                total_cost2 = 0
                offering_exists = False
                for node in data['nodes']:
                    if node.get('node_type') == 'Parts' and node['id'].startswith(product_offering_id):
                        total_cost2 += node.get('cost', 0)
                        offering_exists = True
                total_costs2.append((file_name, i+1, total_cost2))
                print(f"Product offering {product_offering_id} {'exists' if offering_exists else 'does not exist'} in json {i+1} (from {file_name})")
        return total_costs2

    def get_part_cost_by_id(self, part_id):
        for i, file_name in enumerate(os.listdir(self.folder_path)):
            if file_name.endswith('.json'):
                file_path = os.path.join(self.folder_path, file_name)
                data = self.load_json_file(file_path)
                part_exists = False
                for node in data['nodes']:
                    if node['id'] == part_id and node.get('node_type') == 'Parts':
                        part_exists = True
                        print(f"Part {part_id} exists in json {i+1} (from {file_name})")
                        return node.get('cost', 0)
                if not part_exists:
                    print(f"Part {part_id} does not exist in json {i+1} (from {file_name})")
        return None

# Example usage of JSONQuery class
if __name__ == "__main__":
    folder_path = '/home/rm_subhiksha/LAM_SRM/Graph_Generator/v5'
    json_query = JSONQuery(folder_path)

    def memory_usage():
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / (1024 ** 2)  # bytes to MB conversion
    start_time = time.time()
    start_memory = memory_usage()

    # Sum costs for a specific product family prefix
    product_family_id = '1-1'  # Example product family ID
    total_costs_by_family_prefix = json_query.sum_part_costs_by_product_family_prefix(product_family_id)

    # Print the cost of parts for each .json file separately with the .json file name and graph name
    for file_name, json_index, total_cost in total_costs_by_family_prefix:
        print(f"Total cost of all parts under product family prefix {product_family_id} in json {json_index} (from {file_name}): {total_cost}")


    product_offering_id = '1-1-3'  
    total_costs_by_offering_prefix = json_query.sum_part_costs_by_product_offering_prefix(product_offering_id)

    # Print the cost of parts for each .json file separately with the .json file name and graph name
    for file_name, json_index, total_cost2 in total_costs_by_offering_prefix:
        print(f"Total cost of all parts under product offering prefix {product_offering_id} in json {json_index} (from {file_name}): {total_cost2}")

    # Get cost for a specific part
    part_id = '1-1-1-1-1'  # Example part ID
    part_cost = json_query.get_part_cost_by_id(part_id)
    print(f"Cost of part with ID {part_id}: {part_cost}")

    end_memory = memory_usage()
    end_time = time.time()
    time_taken = end_time - start_time
    memory_used = end_memory - start_memory
    print("Time taken in seconds: ", time_taken)
    print("Memory Used in MB: ", memory_used)
