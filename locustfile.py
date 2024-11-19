import os
import json
import time
import logging
from locust import HttpUser, task, between
from json_queries import (
    aggregate_total_revenue_by_business_unit,
    aggregate_parts_nearing_expiry,
    aggregate_average_demand_for_product_offerings,
    aggregate_total_operating_cost_of_facilities,
    aggregate_relationship_costs
)

logging.basicConfig(level=logging.INFO)

class QueryUser(HttpUser):
    wait_time = between(1, 5)
    host = "http://localhost"  # Dummy host to satisfy Locust's requirement

    @task
    def test_aggregate_total_revenue_by_business_unit(self):
        folder_path = "/home/rm_subhiksha/LAM_SRM/Query_jsongraph/static_100_large_dc"
        start_time = time.time()
        result = aggregate_total_revenue_by_business_unit(folder_path)
        end_time = time.time()
        logging.info(f"Result: {result}, Time taken: {end_time - start_time} seconds")

    @task
    def test_aggregate_parts_nearing_expiry(self):
        folder_path = "/home/rm_subhiksha/LAM_SRM/Query_jsongraph/static_100_large_dc"
        threshold = 20
        start_time = time.time()
        result = aggregate_parts_nearing_expiry(folder_path, threshold)
        end_time = time.time()
        logging.info(f"Result: {result}, Time taken: {end_time - start_time} seconds")

    @task
    def test_aggregate_average_demand_for_product_offerings(self):
        folder_path = "/home/rm_subhiksha/LAM_SRM/Query_jsongraph/static_100_large_dc"
        start_time = time.time()
        result = aggregate_average_demand_for_product_offerings(folder_path)
        end_time = time.time()
        logging.info(f"Result: {result}, Time taken: {end_time - start_time} seconds")

    @task
    def test_aggregate_total_operating_cost_of_facilities(self):
        folder_path = "/home/rm_subhiksha/LAM_SRM/Query_jsongraph/static_100_large_dc"
        start_time = time.time()
        result = aggregate_total_operating_cost_of_facilities(folder_path)
        end_time = time.time()
        logging.info(f"Result: {result}, Time taken: {end_time - start_time} seconds")

    @task
    def test_aggregate_relationship_costs(self):
        folder_path = "/home/rm_subhiksha/LAM_SRM/Query_jsongraph/static_100_large_dc"
        start_time = time.time()
        result = aggregate_relationship_costs(folder_path)
        end_time = time.time()
        logging.info(f"Result: {result}, Time taken: {end_time - start_time} seconds")
