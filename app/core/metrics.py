import os

from fastapi import Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest

# Identify which service (ingestion, retrieval, generation, etc.)
APP_NAME = os.getenv("APP_NAME", "rag_architect")


# Global request Counter - — tracked via middleware for every request
# Labels allow metrics to be shown by:
# - App name
# - HTTP method (GET, POST, etc.)
# - endpoint path (/users, /items/{id}, etc.)
# - HTTP status code (200, 404, 500, etc.)
APP_REQUEST_COUNTER = Counter(
    "app_requests_total",  # metric name
    "Total number of HTTP requests",  # description shown in Prometheus
    ["app_name", "method", "endpoint", "http_status"],  # metric dimensions
)


def record_request(method: str, endpoint: str, http_status: str):
    """
    Request each request

    Args:
        method (str): The HTTP method used (e.g. 'GET', 'POST').
        endpoint(str): The path accessed (e.g. '/api/users')
        http_status (str): The response status code (e.g. '200', '404').
    """
    APP_REQUEST_COUNTER.labels(
        app_name=APP_NAME, method=method, endpoint=endpoint, http_status=http_status
    ).inc()  # incr by 1


def metrics_response() -> Response:
    """
    Expose Metrics Endpoint

    Returns:
        fastapi.Response
    """
    # Collect all registered metrics from memory
    data = generate_latest()
    # mimetype - 'text/plain; version=1.0.0; charset=utf-8'
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)
