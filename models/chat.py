from pydantic import BaseModel, Field


class ChatInput(BaseModel):
    prompt: str = Field(..., description="Texto de entrada para el chatbot")
