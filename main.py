from fastapi import FastAPI

# from routes.devices import devices
from routes.network import network
from routes.aichat import aichat
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title="PF-RTXAC",
    description="PF-RTXAC-API",
)

app.include_router(network)
# app.include_router(devices)

app.include_router(aichat)


@app.get("/")
async def root():
    return {"message": "chupapis"}
