from fastapi import APIRouter
from models.network import NetworkInput
from services.subnetting import generate_subnets

# wtf

network = APIRouter()

@network.post("/generate")
async def generate_network(data: NetworkInput):

    result = generate_subnets(data)
    # ...
    # ...

    return result