from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from routes.devices import devices
from routes.network import network
from routes.aichat import aichat
from dotenv import load_dotenv
import os

load_dotenv()

port = os.getenv("PORT")

app = FastAPI(
    title="PF-RTXAC",
    description="PF-RTXAC-API",
    port=port,
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],  # Métodos permitidos (GET, POST, etc.)
    allow_headers=["*"],  # Encabezados permitidos
)

app.include_router(network)
# app.include_router(devices)

app.include_router(aichat)


@app.get("/")
async def root():
    return {"message": "chupapis"}
