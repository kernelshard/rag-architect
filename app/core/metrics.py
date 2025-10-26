from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

from fastapi import Response


# A Counter metric that tracks total HTTP requests.
# Labels allow metrics to be shown by:
# - HTTP method (GET, POST, etc.)
# - endpoint path (/users, /items/{id}, etc.)
# - HTTP status code (200, 404, 500, etc.)
REQUEST_COUNTER = Counter(
    "app_requests_total",  # metric name
    "Total number of HTTP requests",  # description shown in Prometheus
    ["method", "endpoint", "http_status"],  # metric dimensions
)


def record_request(method: str, endpoint: str, http_status: str):
    """
    Request each request

    Args:
        method (str): The HTTP method used (e.g. 'GET', 'POST').
        endpoint(str): The path accessed (e.g. '/api/users')
        http_status (str): The response status code (e.g. '200', '404').
    """
    REQUEST_COUNTER.labels(
        method=method, endpoint=endpoint, http_status=http_status
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
