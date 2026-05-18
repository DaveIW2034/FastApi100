from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List

app = FastAPI(title="Simple Service Registry")

services: Dict[str, List[dict]] = {}


class ServiceInstance(BaseModel):
    service_name: str
    host: str
    port: int


@app.post("/register")
def register(instance: ServiceInstance):
    services.setdefault(instance.service_name, [])

    item = {
        "host": instance.host,
        "port": instance.port,
    }

    if item not in services[instance.service_name]:
        services[instance.service_name].append(item)

    return {
        "message": "registered",
        "service_name": instance.service_name,
        "instances": services[instance.service_name],
    }


@app.get("/discover/{service_name}")
def discover(service_name: str):
    instances = services.get(service_name)

    if not instances:
        raise HTTPException(status_code=404, detail="service not found")

    return {
        "service_name": service_name,
        "instances": instances,
    }


@app.delete("/unregister")
def unregister(instance: ServiceInstance):
    instances = services.get(instance.service_name)

    if not instances:
        raise HTTPException(status_code=404, detail="service not found")

    item = {
        "host": instance.host,
        "port": instance.port,
    }

    if item in instances:
        instances.remove(item)

    return {
        "message": "unregistered",
        "service_name": instance.service_name,
        "instances": instances,
    }