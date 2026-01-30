"""
ログファイル（app.log）を返却する API。

- from / to（ISO8601）で期間指定可能
- JSONログをそのまま返却
"""

from datetime import datetime
import json
from pathlib import Path

from fastapi import APIRouter, Query, HTTPException

router = APIRouter(tags=["logs"])

LOG_FILE = Path("logs/app.log")


@router.get("/logs")
def read_logs(
    from_: datetime | None = Query(None, alias="from"),
    to: datetime | None = Query(None),
):
    if not LOG_FILE.exists():
        raise HTTPException(status_code=404, detail="log file not found")

    results: list[dict] = []

    with LOG_FILE.open(encoding="utf-8") as f:
        for line in f:
            try:
                log = json.loads(line)
            except Exception:
                continue

            ts = datetime.fromisoformat(log["timestamp"])

            if from_ and ts < from_:
                continue
            if to and ts > to:
                continue

            results.append(log)

    return results
