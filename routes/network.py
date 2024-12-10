from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import JSONResponse

from models.network import NetworkInput
from services.subnetting import generate_subnets

from tests.test_recursive_routing_final import generate_output

# wtf

network = APIRouter()

# Definir un modelo de Pydantic para la validación del JSON recibido
class Connection(BaseModel):
    child_names: str
    connections: list
    hosts: int = None  # Aseguramos que 'hosts' es opcional

class RedCentral(BaseModel):
    child_names: str
    connections: list

    
@network.post("/generar-red")
async def subnet_allocation(red_central: RedCentral):
    # Convertimos el modelo Pydantic a un diccionario para usarlo en `generate_output`
    red_central_dict = red_central.model_dump()

    # Llamamos a la función para generar el JSON de salida
    output_dict = generate_output(red_central_dict)

    # Retornamos el JSON generado
    return JSONResponse(content=output_dict, status_code=200)