import logging
import time
from contextvars import ContextVar, Token
from uuid import uuid4

from starlette.datastructures import Headers, MutableHeaders

logger = logging.getLogger("app")

_trace_id_ctx_var: ContextVar[str] = ContextVar("trace_id", default="-")


def generate_trace_id() -> str:
    return uuid4().hex


def get_trace_id() -> str:
    return _trace_id_ctx_var.get()


def set_trace_id(trace_id: str) -> Token:
    return _trace_id_ctx_var.set(trace_id)


def reset_trace_id(token: Token) -> None:
    _trace_id_ctx_var.reset(token)


class TraceIDMiddleware:
    def __init__(self, app, header_name: str = "X-Trace-Id") -> None:
        self.app = app
        self.header_name = header_name

    async def __call__(self, scope, receive, send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        start_time = time.perf_counter()
        headers = Headers(scope=scope)
        trace_id = headers.get(self.header_name) or generate_trace_id()
        token = set_trace_id(trace_id)
        scope.setdefault("state", {})["trace_id"] = trace_id

        method = scope.get("method", "-")
        path = scope.get("path", "-")
        query_string = (scope.get("query_string") or b"").decode("utf-8", errors="ignore")
        client = scope.get("client")
        client_host = client[0] if client else "-"
        client_port = client[1] if client else "-"

        # 请求前日志
        logger.info(
            "request.start method=%s path=%s query=%s client=%s:%s trace_id=%s",
            method,
            path,
            query_string,
            client_host,
            client_port,
            trace_id,
        )

        async def send_wrapper(message) -> None:
            if message["type"] == "http.response.start":
                status_code = message.get("status", 0)
                elapsed_ms = (time.perf_counter() - start_time) * 1000
                response_headers = MutableHeaders(scope=message)
                response_headers[self.header_name] = trace_id

                # 响应返回前日志
                logger.info(
                    "request.end method=%s path=%s status=%s duration_ms=%.2f trace_id=%s",
                    method,
                    path,
                    status_code,
                    elapsed_ms,
                    trace_id,
                )
            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)
        finally:
            reset_trace_id(token)
