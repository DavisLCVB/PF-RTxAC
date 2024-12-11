from fastapi import APIRouter
from services.routing import *
from models.network import NetworkInputSubnet
from services.scripts import generate_scripts

network = APIRouter()


@network.post("/generar-red")
async def generate_network(red_central: NetworkInputSubnet):
    red = subneteo(
        red_central.red, red_central.base_ip, red_central.mask, red_central.table
    )
    router = red["central_router"]
    connections = red["ip_connections"]
    script = generate_scripts(router, connections)
    return {"router": router, "connections": connections, "script": script}
