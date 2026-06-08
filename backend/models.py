from pydantic import BaseModel

class ChatRequest(BaseModel):
    query: str
    agent: str = "auto"