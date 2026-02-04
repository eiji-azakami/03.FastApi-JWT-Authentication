"""
HTTP 例外のハンドラー。

- stacktrace を含め出力
"""

import logging
import traceback
from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger("error")


async def global_exception_handler(request: Request, exc: Exception):
    """
    グローバル例外ハンドラー

    Args:
        request (Request): リクエスト情報
        exc (Exception): 発生した例外

    Returns:
        JSONResponse: HTTP 500エラー
    """
    logger = logging.getLogger("error")
    logger.error("Unhandled exception occurred")
    logger.error("Traceback: %s", traceback.format_exc())
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )
