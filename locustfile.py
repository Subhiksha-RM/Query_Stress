import os
import json
import time
import logging
from locust import HttpUser, task, between, events
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

    def on_start(self):
        self.start_time = time.time()

    def on_stop(self):
        end_time = time.time()
        total_time = end_time - self.start_time
        user_count = self.environment.runner.user_count
        logging.info(f"Total time for test: {total_time} seconds, Number of users: {user_count}")

    def log_event(self, request_type, name, start_time, result=None, exception=None):
        end_time = time.time()
        response_time = (end_time - start_time) * 1000  # Convert to milliseconds
        response_length = len(result) if isinstance(result, (list, str)) else 0
        if exception:
            events.request.fire(request_type=request_type, name=name, response_time=response_time, response_length=response_length, exception=exception)
            logging.error(f"Error: {exception}, Time taken: {response_time} ms")
        else:
            events.request.fire(request_type=request_type, name=name, response_time=response_time, response_length=response_length)
            logging.info(f"Result: {result}, Time taken: {response_time} ms")

    @task
    def test_aggregate_total_revenue_by_business_unit(self):
        folder_path = "/home/rm_subhiksha/LAM_SRM/Query_jsongraph/static_100_large_dc"
        start_time = time.time()
        try:
            result = aggregate_total_revenue_by_business_unit(folder_path)
            self.log_event("query", "aggregate_total_revenue_by_business_unit", start_time, result)
        except Exception as e:
            self.log_event("query", "aggregate_total_revenue_by_business_unit", start_time, exception=e)

    @task
    def test_aggregate_parts_nearing_expiry(self):
        folder_path = "/home/rm_subhiksha/LAM_SRM/Query_jsongraph/static_100_large_dc"
        threshold = 20
        start_time = time.time()
        try:
            result = aggregate_parts_nearing_expiry(folder_path, threshold)
            self.log_event("query", "aggregate_parts_nearing_expiry", start_time, result)
        except Exception as e:
            self.log_event("query", "aggregate_parts_nearing_expiry", start_time, exception=e)

    @task
    def test_aggregate_average_demand_for_product_offerings(self):
        folder_path = "/home/rm_subhiksha/LAM_SRM/Query_jsongraph/static_100_large_dc"
        start_time = time.time()
        try:
            result = aggregate_average_demand_for_product_offerings(folder_path)
            self.log_event("query", "aggregate_average_demand_for_product_offerings", start_time, result)
        except Exception as e:
            self.log_event("query", "aggregate_average_demand_for_product_offerings", start_time, exception=e)

    @task
    def test_aggregate_total_operating_cost_of_facilities(self):
        folder_path = "/home/rm_subhiksha/LAM_SRM/Query_jsongraph/static_100_large_dc"
        start_time = time.time()
        try:
            result = aggregate_total_operating_cost_of_facilities(folder_path)
            self.log_event("query", "aggregate_total_operating_cost_of_facilities", start_time, result)
        except Exception as e:
            self.log_event("query", "aggregate_total_operating_cost_of_facilities", start_time, exception=e)

    @task
    def test_aggregate_relationship_costs(self):
        folder_path = "/home/rm_subhiksha/LAM_SRM/Query_jsongraph/static_100_large_dc"
        start_time = time.time()
        try:
            result = aggregate_relationship_costs(folder_path)
            self.log_event("query", "aggregate_relationship_costs", start_time, result)
        except Exception as e:
            self.log_event("query", "aggregate_relationship_costs", start_time, exception=e)
