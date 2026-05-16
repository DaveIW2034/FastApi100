import logging

from fastapi import Request
from fastapi.testclient import TestClient

from app.main import create_app


def test_trace_id_added_to_request_and_response():
    app = create_app()
    logger = logging.getLogger("app")
    records = []

    class ListHandler(logging.Handler):
        def emit(self, record):
            records.append(record)

    @app.get("/trace-test")
    async def trace_test(request: Request):
        logger.info("trace middleware test")
        return {"trace_id": request.state.trace_id}

    handler = ListHandler()
    logger.addHandler(handler)

    try:
        client = TestClient(app)
        response = client.get("/trace-test")
    finally:
        logger.removeHandler(handler)

    assert response.status_code == 200
    response_trace_id = response.headers["X-Trace-Id"]
    assert response_trace_id
    assert response.json()["trace_id"] == response_trace_id
    assert records[-1].trace_id == response_trace_id


def test_trace_id_reuses_request_header():
    app = create_app()

    @app.get("/trace-test-header")
    async def trace_test_header(request: Request):
        return {"trace_id": request.state.trace_id}

    client = TestClient(app)
    response = client.get("/trace-test-header", headers={"X-Trace-Id": "custom-trace-id"})

    assert response.status_code == 200
    assert response.headers["X-Trace-Id"] == "custom-trace-id"
    assert response.json()["trace_id"] == "custom-trace-id"
