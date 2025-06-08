from fastapi import FastAPI
from routes import router
from fastapi.middleware.cors import CORSMiddleware

print("🚀 Starting FastAPI App...")

app = FastAPI(
    title="Student Schedule QA Bot",
    version="0.1"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"message": "test"}

# Register routes
app.include_router(router)
