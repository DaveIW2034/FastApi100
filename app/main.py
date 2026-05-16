import logging

import uvicorn
from fastapi import FastAPI

from app.api.v1 import user
from app.logging_config import setup_logging
from app.middleware.trace import TraceIDMiddleware


setup_logging()
logger = logging.getLogger("app")


def create_app() -> FastAPI:
    app = FastAPI(title="My FastAPI App")
    app.add_middleware(TraceIDMiddleware)
    app.logger = logger
    # 注册路由
    app.include_router(user.router, prefix="/api/v1/user", tags=["User"])
    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
