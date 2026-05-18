from fastapi import FastAPI
import requests
import random

app = FastAPI(title="User Service")

REGISTRY_URL = "http://localhost:8001"


@app.get("/user/orders")
def get_user_orders():
    result = requests.get(f"{REGISTRY_URL}/discover/order-service").json()

    instances = result["instances"]
    instance = random.choice(instances)

    url = f"http://{instance['host']}:{instance['port']}/orders"

    orders = requests.get(url).json()

    return {
        "called_service": url,
        "orders": orders,
    }