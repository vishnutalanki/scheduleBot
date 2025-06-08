from fastapi import APIRouter, HTTPException
from models import LoginRequest, ChatRequest, ChatResponse
from database import supabase
from ai_engine import scheduleQA
import json

router = APIRouter()

# Temporary in-memory cache for schedule data
student_data_cache = {}

@router.post("/login")
def login(request: LoginRequest):
    student_id = request.student_id
    student_id = request.student_id.strip().upper()
    print("🧪 student_id received:", student_id)
    # Fetch from Supabase
    response = supabase.table("student_schedule").select("*").ilike("student_id", f"%{student_id.strip()}%").execute()
    # response = supabase.table("student_schedule").select("*").limit(1).execute()
    print("Test query result:", response.data)
    
    if not response.data:
        raise HTTPException(status_code=404, detail="Student not found")

    student_data_cache[student_id] = response.data
    return {"message": "Login successful", "student_id": student_id}

# @router.post("/chat")
# def chat(request: ChatRequest):
#     if request.student_id not in student_data_cache:
#         raise HTTPException(status_code=403, detail="Please log in first.")

#     return {"message": "Message received. Use /response to get the AI answer."}

@router.post("/response", response_model=ChatResponse)
def respond(request: ChatRequest):
    schedule_data = student_data_cache.get(request.student_id)
    print("🎯 schedule used in GPT:", schedule_data)
    if not schedule_data:
        raise HTTPException(status_code=403, detail="No schedule found. Please log in again.")
    formatted_data = json.dumps(schedule_data, indent=2)
    print("🎯 formatted data for GPT:", formatted_data)
    ai_answer = scheduleQA(request.message, formatted_data)
    return ChatResponse(answer=ai_answer)
