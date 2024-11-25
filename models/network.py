from pydantic import BaseModel, Field

class NetworkInput(BaseModel):

    base_ip: str = Field(..., description="IP base de la red")
    num_edificios: int = Field(..., description="Cantidad de edificios")
    pisos_por_edificio: list[int] = Field(..., description=" Cantidad de pisos por edificio")

