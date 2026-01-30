"""
logging 設定。

- JSON ログ
- request_id / method / path 自動付与
- stdout(標準出力) + 日次ローテーションファイル
"""

import json
import logging
from logging.handlers import TimedRotatingFileHandler

from app.middlewares.logging_context import get_request_id, request_method, request_path


class RequestContextFilter(logging.Filter):
    """
    LogRecord に request 情報注入する Filter
    """

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = get_request_id() or "-"
        record.method = request_method.get() or "-"
        record.path = request_path.get() or "-"
        return True


class JsonFormatter(logging.Formatter):
    """
    JSON 形式でログを出力する Formatter
    """

    def format(self, record: logging.LogRecord) -> str:
        log = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "request_id": record.request_id,
            "method": record.method,
            "path": record.path,
            "message": record.getMessage(),
        }

        if record.exc_info:
            log["exception"] = self.formatException(record.exc_info)

        return json.dumps(log, ensure_ascii=False)


def setup_logging(level: int = logging.INFO) -> None:
    """
    アプリケーション全体の logging 初期化処理
    """

    formatter = JsonFormatter()

    context_filter = RequestContextFilter()

    # stdout(標準出力)
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    console.addFilter(context_filter)

    # 日次ローテーションファイル
    #  14日間 保持
    file_handler = TimedRotatingFileHandler(
        filename="logs/app.log",
        when="midnight",
        interval=1,
        backupCount=14,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    file_handler.addFilter(context_filter)

    logging.basicConfig(
        level=level,
        handlers=[console, file_handler],
    )
