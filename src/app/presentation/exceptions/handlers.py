import logging
import traceback
from typing import Any, Optional

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


def setup_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        logger.warning(
            "Request validation error",
            extra={
                "path": request.url.path,
                "method": request.method,
                "errors": exc.errors(),
            },
        )

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder(
                {
                    "message": "Validation Error",
                    "detail": exc.errors(),
                    "debug": debug_response(request) if app.debug else None,
                }
            ),
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request, exc: HTTPException
    ) -> JSONResponse:
        logger.error(
            "HTTP Exception",
            extra={
                "path": request.url.path,
                "method": request.method,
                "status_code": exc.status_code,
                "detail": exc.detail,
            },
        )

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "message": exc.detail,
                "debug": debug_response(request) if app.debug else None,
            },
        )

    @app.exception_handler(Exception)
    async def unexpected_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        logger.critical(
            "Unhandled exception",
            extra={
                "path": request.url.path,
                "method": request.method,
                "error": str(exc),
                "traceback": traceback.format_exc(),
            },
            exc_info=True,
        )

        content = {
            "message": "Internal Server Error",
            "debug": debug_response(request, exc) if app.debug else None,
        }

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=content,
        )


def debug_response(request: Request, exc: Optional[Exception] = None) -> dict[str, Any]:
    debug_info = {
        "path": request.url.path,
        "method": request.method,
        "params": dict(request.path_params),
        "client": f"{request.client.host}:{request.client.port}"
        if request.client
        else None,
    }

    if exc:
        debug_info["exception_type"] = exc.__class__.__name__
        debug_info["exception_message"] = str(exc)
        if isinstance(exc, RequestValidationError):
            debug_info["request_body"] = exc.body

    if request.url.path not in ["/docs", "/redoc", "/openapi.json"]:
        debug_info["headers"] = dict(request.headers)

    return debug_info
