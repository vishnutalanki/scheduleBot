from pydantic import BaseModel
from typing import Optional

class LoginRequest(BaseModel):
    student_id: str

class ChatRequest(BaseModel):
    student_id: str
    message: str

class ChatResponse(BaseModel):
    answer: str
