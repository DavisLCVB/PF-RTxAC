from fastapi import FastAPI
#from routes.devices import devices
from routes.network import network

app = FastAPI(

    title="PF-RTXAC",
    description="PF-RTXAC-API",
)

app.include_router(network)
#app.include_router(devices)

@app.get("/")
async def root():
    return {"message": "chupapis"}