from fastapi import FastAPI
import requests

app = FastAPI(title="Order Service")

REGISTRY_URL = "http://localhost:8001"


@app.on_event("startup")
def register_service():
    requests.post(
        f"{REGISTRY_URL}/register",
        json={
            "service_name": "order-service",
            "host": "localhost",
            "port": 9002,
        },
    )


@app.get("/orders")
def list_orders():
    return [
        {"id": 1, "name": "订单A"},
        {"id": 2, "name": "订单B"},
    ]