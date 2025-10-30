from collections.abc import Callable
from typing import Any
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from time import perf_counter
from backend.utils.logging import logger


class LoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Any]
    ) -> Response:
        """
        Logs all incoming and outgoing request, response pairs. This method logs the request params,
        datetime of request, duration of execution. Logs should be printed using the custom logging module provided.
        Logs should be printed so that they are easily readable and understandable.

        :param request: Request received to this middleware from client (it is supplied by FastAPI)
        :param call_next: Endpoint or next middleware to be called (if any, this is the next middleware in the chain of middlewares, it is supplied by FastAPI)
        :return: Response from endpoint
        """
        start = perf_counter()

        # Basic request info
        method = request.method
        url_path = request.url.path
        query_params = dict(request.query_params)

        # Try to read JSON body safely (without consuming stream for non-JSON)
        body_preview: Any
        try:
            body_preview = await request.json()
        except Exception:
            body_preview = None

        logger.info(
            f"HTTP Request | method={method} path={url_path} query={query_params} body={body_preview}"
        )

        response = await call_next(request)

        duration_ms = (perf_counter() - start) * 1000
        logger.info(
            f"HTTP Response | method={method} path={url_path} status={response.status_code} duration_ms={duration_ms:.2f}"
        )

        return response
