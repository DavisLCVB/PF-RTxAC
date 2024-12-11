from fastapi import APIRouter
from services.openai import generateResponse
from models.chat import ChatInput
import json
aichat = APIRouter()


@aichat.post("/chat")
async def chat(prompt: ChatInput):
    return generateResponse(prompt.prompt)