import networkx as nx
import matplotlib.pyplot as plt
import time 
import psutil
import os
from datetime import datetime, timedelta
import random

def memory_usage():
    process=psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 ** 2) #bytes to mb conversion

def generate_supply_chain_graph(total_nodes=1000):
    # Initialize directed graph
    G = nx.DiGraph()
    
    # Distribution of nodes (approximate percentages)
    node_distribution = {
        'Parts': int(total_nodes * 0.5),  # 40% parts
        'Supplier': int(total_nodes * 0.3),  # 25% suppliers
        'Warehouse': int(total_nodes * 0.2),  # 15% warehouses
        'Product': 5,  
        'BusinessUnit': 1
    }
    
    # Generate node data
    def generate_dates():
        start_date = datetime(2024, 1, 1)
        valid_from = start_date + timedelta(days=random.randint(0, 365))
        valid_to = valid_from + timedelta(days=random.randint(180, 730))
        return valid_from.strftime('%Y-%m-%d'), valid_to.strftime('%Y-%m-%d')
    
    parts = ['Aluminum', 'Steel', 'Plastic', 'Copper', 'Rubber', 'Glass', 'Silicon', 'Carbon Fiber']
    countries = ['USA', 'China', 'Germany', 'Japan', 'Mexico', 'India', 'UK', 'Brazil', 'Italy', 'Canada']

    # Generate Parts nodes
    for i in range(node_distribution['Parts']):
        valid_from, valid_to = generate_dates()
        G.add_node(f'P{i}', 
                  type='Parts',
                  part_group=f'Group {random.randint(1, 20)}',
                  part_family=f'Family {random.randint(1, 10)}',
                  raw_material=random.choice(parts))
    
    # Generate Supplier nodes
    for i in range(node_distribution['Supplier']):
        G.add_node(f'S{i}',
                  type='Supplier',
                  name=f'Supplier {i}',
                  country=random.choice(countries))
    
    # Generate Warehouse nodes
    for i in range(node_distribution['Warehouse']):
        G.add_node(f'W{i}',
                  type='Warehouse',
                  name=f'Warehouse {i}',
                  country=random.choice(countries))
    
    # Generate Product nodes
    for i in range(node_distribution['Product']):
        G.add_node(f'PR{i}',
                  type='Product',
                  product_family=f'Product Family {i}')
    
    # Generate Business Unit nodes
    for i in range(node_distribution['BusinessUnit']):
        G.add_node(f'BU{i}',
                  type='BusinessUnit',
                  name=f'Business Unit {i}')
    
    # Generate edges
    parts = [n for n in G.nodes() if n.startswith('P')]
    suppliers = [n for n in G.nodes() if n.startswith('S')]
    warehouses = [n for n in G.nodes() if n.startswith('W')]
    products = [n for n in G.nodes() if n.startswith('PR')]
    business_units = [n for n in G.nodes() if n.startswith('BU')]
    
    # Part-Part relationships
    for part in parts:
        num_connections = random.randint(0, 3)
        for _ in range(num_connections):
            other_part = random.choice(parts)
            if part != other_part:
                valid_from, valid_to = generate_dates()
                G.add_edge(part, other_part, 
                          relationship='Part-Part',
                          plant=f'Plant_{random.randint(1,5)}',
                          qty=random.randint(1, 100),
                          valid_from=valid_from,
                          valid_to=valid_to,
                          item_cat=f'Category_{random.randint(1,10)}')
    
    # Supplier-Part relationships
    for supplier in suppliers:
        num_parts = random.randint(5, 15)
        for _ in range(num_parts):
            part = random.choice(parts)
            G.add_edge(supplier, part,
                      relationship='Supplier-Part',
                      preferred_supplier=random.choice([True, False]))
            # Add PO relationship
            G.add_edge(supplier, part,
                      relationship='Supplier-PO',
                      po_open=random.randint(0, 10),
                      po_closed=random.randint(0, 20),
                      po_total=random.randint(20, 50))
    
    # Part-Warehouse relationships
    for part in parts:
        warehouse = random.choice(warehouses)
        G.add_edge(part, warehouse,
                  relationship='Part-Warehouse',
                  inventory=random.randint(0, 1000),
                  lead_time=random.randint(1, 30),
                  production_time=random.randint(1, 14),
                  safety_stock=random.randint(50, 200))
    
    # Part-Product relationships
    for product in products:
        num_parts = random.randint(5, 20)
        for _ in range(num_parts):
            part = random.choice(parts)
            G.add_edge(part, product,
                      relationship='Part-Product')
    
    # Product-Business Unit relationships
    for product in products:
        business_unit = random.choice(business_units)
        G.add_edge(product, business_unit,
                  relationship='Product-Business')
    
    return G


def get_edge_attr(g_1k):
    sub_graph3 = nx.ego_graph(g_1k, 'PR1', radius=5, center=True, undirected=False, distance=None)
    edges_warehouse = [(u, v) for u, v, attr in sub_graph3.edges(data=True) if attr.get('production_time', 0) > 2]

    # Create a subgraph from the filtered edges
    subg = sub_graph3.edge_subgraph(edges_warehouse).copy()

    # Print nodes and edges of the subgraph
    print("Nodes in the graph: ", subg.nodes())
    print("Edges in the graph: ", subg.edges(data=True))


if __name__ == "__main__":

    start_time = time.time()
    start_memory = memory_usage()
    g_1k = generate_supply_chain_graph(total_nodes=1000000)
    end_memory = memory_usage()
    end_time = time.time()
    time_taken = end_time - start_time
    memory_used = end_memory - start_memory
    print("Time taken in seconds: ", time_taken)
    print("Memory Used in MB: ", memory_used)


    start_time = time.time()
    start_memory = memory_usage()
    get_edge_attr(g_1k)
    end_memory = memory_usage()
    end_time = time.time()
    time_taken = end_time - start_time
    memory_used = end_memory - start_memory
    print("Time taken in seconds: ", time_taken)
    print("Memory Used in MB: ", memory_used)
