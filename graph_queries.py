import os
import json
import networkx as nx
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

def total_revenue_by_business_unit(graphs):
    aggregated_revenue = {}
    for i, (G, file_name) in enumerate(graphs):
        revenue_by_unit = {}
        for node_id, node_data in G.nodes(data=True):
            if node_data.get('node_type') == 'BusinessUnit':
                unit = node_data['name']
                revenue = node_data['revenue']
                if unit in revenue_by_unit:
                    revenue_by_unit[unit] += revenue
                else:
                    revenue_by_unit[unit] = revenue
        if revenue_by_unit:
            print(f"Aggregated Revenue by Business Unit for {file_name}: {revenue_by_unit}")
            for unit, revenue in revenue_by_unit.items():
                if unit in aggregated_revenue:
                    aggregated_revenue[unit] += revenue
                else:
                    aggregated_revenue[unit] = revenue
        else:
            print(f"No Business Unit found in {file_name}")
    return aggregated_revenue

def parts_nearing_expiry(graphs, threshold):
    total_parts_near_expiry = 0
    for i, (G, file_name) in enumerate(graphs):
        parts_near_expiry = []
        for node_id, node_data in G.nodes(data=True):
            if node_data.get('node_type') == 'Parts' and node_data.get('expiry', 0) <= threshold:
                parts_near_expiry.append(node_id)
        if parts_near_expiry:
            print(f"Parts Nearing Expiry for {file_name}: {parts_near_expiry}")
        else:
            print(f"No Parts Nearing Expiry found in {file_name}")
        total_parts_near_expiry += len(parts_near_expiry)
    return total_parts_near_expiry

def average_demand_for_product_offerings(graphs):
    total_demand = 0
    count = 0
    for i, (G, file_name) in enumerate(graphs):
        demand = sum(node_data['demand'] for node_id, node_data in G.nodes(data=True) if node_data['node_type'] == 'ProductOffering')
        product_offerings_count = sum(1 for node_id, node_data in G.nodes(data=True) if node_data['node_type'] == 'ProductOffering')
        if product_offerings_count > 0:
            print(f"Average Demand for Product Offerings in {file_name}: {demand / product_offerings_count}")
        else:
            print(f"No Product Offerings found in {file_name}")
        total_demand += demand
        count += product_offerings_count
    return total_demand / count if count > 0 else 0

def total_operating_cost_of_facilities(graphs):
    total_cost = 0
    for i, (G, file_name) in enumerate(graphs):
        cost = sum(node_data['operating_cost'] for node_id, node_data in G.nodes(data=True) if node_data['node_type'] == 'Facility')
        if cost > 0:
            print(f"Total Operating Cost of Facilities in {file_name}: {cost}")
        else:
            print(f"No Facilities found in {file_name}")
        total_cost += cost
    return total_cost

def relationship_costs(graphs):
    total_transportation_cost = 0
    total_storage_cost = 0
    for i, (G, file_name) in enumerate(graphs):
        transport_cost = sum(edge_data['transportation_cost'] for _, _, edge_data in G.edges(data=True) if 'transportation_cost' in edge_data)
        storage_cost = sum(edge_data['storage_cost'] for _, _, edge_data in G.edges(data=True) if 'storage_cost' in edge_data)
        if transport_cost > 0 or storage_cost > 0:
            print(f"Relationship Costs in {file_name}: Transportation Cost = {transport_cost}, Storage Cost = {storage_cost}")
        else:
            print(f"No Relationship Costs found in {file_name}")
        total_transportation_cost += transport_cost
        total_storage_cost += storage_cost
    return total_transportation_cost, total_storage_cost

def aggregate_relationship_costs(graphs):
    return relationship_costs(graphs)

