"""
アクセスログ用ミドルウェア。

- Request-ID の生成
- 開始ログ / 終了ログ
- elapsed_ms の計測
- ContextVar の set / reset
"""

import logging
import time
import uuid

from fastapi import Request, Response

from app.middlewares.logging_context import (
    request_method,
    request_path,
    set_request_id,
)

logger = logging.getLogger("access")


async def access_log_middleware(request: Request, call_next) -> Response:
    request_id = uuid.uuid4().hex
    set_request_id(request_id)

    start = time.time()

    token_method = request_method.set(request.method)
    token_path = request_path.set(request.url.path)

    logger.info("request start")

    try:
        response = await call_next(request)
        return response
    finally:
        elapsed_ms = int((time.time() - start) * 1000)
        logger.info("request end elapsed_ms=%d", elapsed_ms)

        # ContextVar を必ず元に戻す
        request_method.reset(token_method)
        request_path.reset(token_path)
