from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ai.chat import chat_with_ai

# ✅ FIRST create app
app = FastAPI()

# ✅ THEN add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "AI Assistant Running 🚀"}

@app.get("/chat")
async def chat(message: str):
    response = await chat_with_ai(message)
    return {"response": response}

