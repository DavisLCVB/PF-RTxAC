from pydantic import BaseModel, Field


class NetworkInput(BaseModel):

    base_ip: str = Field(..., description="IP base de la red")
    num_edificios: int = Field(..., description="Cantidad de edificios")
    pisos_por_edificio: list[int] = Field(
        ..., description=" Cantidad de pisos por edificio"
    )
    max_pcs_por_piso: int = Field(
        ..., description="Máximo de computadoras en cualquier piso de un edificio"
    )


class NetworkInputSubnet(BaseModel):
    base_ip: str = Field(..., description="IP base de la red")
    mask: int = Field(..., description="Prefijo de la red")
    red: dict
    table: list[dict]
