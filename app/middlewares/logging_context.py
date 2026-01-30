"""
logging 用 ContextVar 定義。

- request_id
- HTTP method
- request path

ミドルウェアで set / reset され、
logging.Filter / Formatter から参照される。
"""

from contextvars import ContextVar

_request_id: ContextVar[str | None] = ContextVar("request_id", default=None)
request_method: ContextVar[str | None] = ContextVar("request_method", default=None)
request_path: ContextVar[str | None] = ContextVar("request_path", default=None)


def set_request_id(request_id: str) -> None:
    _request_id.set(request_id)


def get_request_id() -> str | None:
    return _request_id.get()
