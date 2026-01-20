from dotenv import load_dotenv
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Load .env early
load_dotenv()
print("OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY"))

from knowledge_base import KnowledgeBase
from model_handler import generate_reply

app = FastAPI()

# Enable CORS for frontend (adjust URL if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://127.0.0.1:5500"] if you serve frontend locally
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load knowledge at startup
kb = KnowledgeBase()
kb.load_knowledge("data/client_1.txt")

class UserMessage(BaseModel):
    message: str

@app.get("/")
def home():
    return {"status": "AI bot backend running"}

@app.post("/chat")
async def chat(user_msg: UserMessage):
    user_input = user_msg.message

    # Retrieve relevant chunks
    context = kb.search(user_input, top_k=3)

    # Generate response
    reply = generate_reply(user_input, context)

    return {"reply": reply}