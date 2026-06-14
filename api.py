from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware 
from app import ask

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(BaseModel):
    question: str

@app.get("/")
def root():
    return {"message": "CollegeBot API is running!"}

@app.post("/ask")
def ask_question(q: Question):
    answer = ask(q.question)
    return {"question": q.question, "answer": answer}