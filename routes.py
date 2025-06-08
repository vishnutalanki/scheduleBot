from fastapi import APIRouter, HTTPException
from models import ChatRequest, ChatResponse, LoginRequest
from ai_engine import scheduleQA
from database import supabase
import json

router = APIRouter()

@router.post("/login")
def login(request: LoginRequest):
    student_id = request.student_id
    print("🧪 student_id received:", student_id)

    # Validate existence of student in schedule table
    response = supabase.table("student_schedule").select("*").eq("student_id", student_id).limit(1).execute()
    result = response.data
    print("🟦 Supabase raw result:", result)

    if not result:
        raise HTTPException(status_code=404, detail="Student not found")

    return {"message": "Login successful", "student_id": student_id}


@router.post("/response", response_model=ChatResponse)
def respond(request: ChatRequest):
    student_id = request.student_id
    question = request.message

    # Always pull fresh schedule data per request
    response = supabase.table("student_schedule").select("*").ilike("student_id", f"%{student_id.strip()}%").execute()
    
    schedule_data = response.data

    if not schedule_data:
        raise HTTPException(status_code=403, detail="No schedule found. Please log in again.")

    print("🎯 schedule used in GPT:", schedule_data)

    formatted_data = json.dumps(schedule_data, indent=2)
    print("🎯 formatted data for GPT:", formatted_data)

    ai_answer = scheduleQA(question, formatted_data)
    return ChatResponse(answer=ai_answer)