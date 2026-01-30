from fastapi import FastAPI

from app.config.logging_config import setup_logging
from app.middlewares.access_log import access_log_middleware
from app.api.logs import router as logs_router
from app.api.auth import router as auth_router
from app.exceptions.handlers import unhandled_exception_handler

setup_logging()

app = FastAPI(title="FastAPI JWT認証 サンプル")

app.middleware("http")(access_log_middleware)
app.add_exception_handler(Exception, unhandled_exception_handler)

app.include_router(logs_router)
app.include_router(auth_router)


@app.get("/health")
def health():
    return {"status": "ok"}
