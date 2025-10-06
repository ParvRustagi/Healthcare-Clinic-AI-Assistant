from pydantic import BaseModel

class ChatRequest(BaseModel):
    session_id: str = "default"
    text: str

class ChatResponse(BaseModel):
    reply: str
