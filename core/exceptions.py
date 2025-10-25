from typing import Any, Dict
from fastapi import status, FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException


class AppException(Exception):
    """
    Custom Exception Definition
    """

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        payload: Dict[str, Any] | None = None,
    ):
        self.message = message
        self.status_code = status_code
        self.payload = payload or {}


def register_exception_handlers(app: FastAPI):
    """
    Registers custom exception handlers to the FastAPI app.
    Handles AppException and HTTPException consistently.
    """

    # Handler for AppException
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        """
        Converts AppException into a JSON response.
        Includes the error message and optional payload details.
        """
        content: Dict[str, Any] = {"error": exc.message}

        # If there is additional payload, include it under 'details'
        if exc.payload:
            content["details"] = exc.payload
        return JSONResponse(status_code=exc.status_code, content=content)

    # Optional: convert HTTPException to JSONResponse (cleaner)
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """
        Converts FastAPI's built-in HTTPException into JSON response.
        Ensures all HTTP errors are returned in a consistent JSON format.
        """
        return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})
