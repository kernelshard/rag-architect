import time
from collections.abc import Callable
from typing import Any

import uvicorn
from fastapi import FastAPI, Request, Response

from .api.router import router as api_router
from .core.config import settings
from .core.exceptions import register_exception_handlers
from .core.logging import configure_logging, get_logger
from .core.metrics import metrics_response, record_request


logger = get_logger(__name__)


# Application Factory
def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    Includes routes, middleware, metrics, and exception handling.
    """
    configure_logging()
    application = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

    # register exception handlers
    register_exception_handlers(app=application)

    # include API router
    application.include_router(api_router)

    # Prometheus Metrics Endpoint
    @application.get("/metrics", include_in_schema=False)
    async def metrics() -> Response:
        return metrics_response()

    #  Middleware: Record basic request metrics
    @application.middleware("http")
    async def metrics_middleware(request: Request, call_next: Callable) -> Response:
        """
        Middleware that:
        - Records request count for Prometheus
        - Adds request processing time to response headers
        """
        start = time.time()
        try:
            response: Response = await call_next(request)
        except Exception:
            logger.exception("Unhandled exception")
            raise

        process_time = round((time.time() - start) * 1000, 2)
        record_request(request.method, request.url.path, str(response.status_code))

        # total processing time recording in header
        response.headers["X-Process-Time-MS"] = str(process_time)
        return response

    @application.get("/", include_in_schema=False)
    async def root() -> dict[str, Any]:
        """
        Sample root route to confirm the app is running
        """
        return {"app": settings.APP_NAME, "env": settings.ENV}

    return application


# App initialization
app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
