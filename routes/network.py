from fastapi import APIRouter
from services.routing import *
from models.network import NetworkInputSubnet

network = APIRouter()


@network.post("/generar-red")
async def generate_network(red_central: NetworkInputSubnet):
    tabla = extract_connections(red_central.red)
    red = subneteo(red_central.red, red_central.base_ip, tabla)
