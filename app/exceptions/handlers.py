"""
HTTP 例外のハンドラー。

- stacktrace を含め出力
"""

import logging

from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger("error")


async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("unhandled exception occurred")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )
