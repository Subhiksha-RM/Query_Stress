import os
import json

def load_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def total_revenue_by_business_unit(data):
    revenue_by_unit = {}
    nodes = data.get('nodes', [])
    for entry in nodes:
        if entry.get('node_type') == 'BusinessUnit':
            unit = entry['name']
            revenue = entry['revenue']
            if unit in revenue_by_unit:
                revenue_by_unit[unit] += revenue
            else:
                revenue_by_unit[unit] = revenue
    return revenue_by_unit

def aggregate_total_revenue_by_business_unit(folder_path):
    aggregated_revenue = {}
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.json'):
            file_path = os.path.join(folder_path, file_name)
            data = load_data(file_path)
            revenue_by_unit = total_revenue_by_business_unit(data)
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

def parts_nearing_expiry(data, threshold):
    nodes = data.get('nodes', [])
    return [node for node in nodes if node.get('node_type') == 'Part' and node.get('expiry_days', 0) <= threshold]

def aggregate_parts_nearing_expiry(folder_path, threshold):
    total_parts_near_expiry = 0
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.json'):
            file_path = os.path.join(folder_path, file_name)
            data = load_data(file_path)
            parts_near_expiry = parts_nearing_expiry(data, threshold)
            if parts_near_expiry:
                print(f"Parts Nearing Expiry for {file_name}: {parts_near_expiry}")
            else:
                print(f"No Parts Nearing Expiry found in {file_name}")
            total_parts_near_expiry += len(parts_near_expiry)
    return total_parts_near_expiry

def aggregate_average_demand_for_product_offerings(folder_path):
    total_demand = 0
    count = 0
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.json'):
            file_path = os.path.join(folder_path, file_name)
            data = load_data(file_path)
            demand = sum(node['demand'] for node in data['nodes'] if node['node_type'] == 'ProductOffering')
            product_offerings_count = sum(1 for node in data['nodes'] if node['node_type'] == 'ProductOffering')
            if product_offerings_count > 0:
                print(f"Average Demand for Product Offerings in {file_name}: {demand / product_offerings_count}")
            else:
                print(f"No Product Offerings found in {file_name}")
            total_demand += demand
            count += product_offerings_count
    return total_demand / count if count > 0 else 0

def total_operating_cost_of_facilities(data):
    nodes = data.get('nodes', [])
    return sum(node['operating_cost'] for node in nodes if node.get('node_type') == 'Facility')

def aggregate_total_operating_cost_of_facilities(folder_path):
    total_cost = 0
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.json'):
            file_path = os.path.join(folder_path, file_name)
            data = load_data(file_path)
            cost = total_operating_cost_of_facilities(data)
            if cost > 0:
                print(f"Total Operating Cost of Facilities in {file_name}: {cost}")
            else:
                print(f"No Facilities found in {file_name}")
            total_cost += cost
    return total_cost

def relationship_costs(data):
    links = data.get('links', [])
    total_transportation_cost = sum(link['transportation_cost'] for link in links if 'transportation_cost' in link)
    total_storage_cost = sum(link['storage_cost'] for link in links if 'storage_cost' in link)
    return total_transportation_cost, total_storage_cost

def aggregate_relationship_costs(folder_path):
    total_transportation_cost = 0
    total_storage_cost = 0
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.json'):
            file_path = os.path.join(folder_path, file_name)
            data = load_data(file_path)
            transport_cost, storage_cost = relationship_costs(data)
            if transport_cost > 0 or storage_cost > 0:
                print(f"Relationship Costs in {file_name}: Transportation Cost = {transport_cost}, Storage Cost = {storage_cost}")
            else:
                print(f"No Relationship Costs found in {file_name}")
            total_transportation_cost += transport_cost
            total_storage_cost += storage_cost
    return total_transportation_cost, total_storage_cost
