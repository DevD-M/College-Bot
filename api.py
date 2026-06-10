from fastapi import FastAPI
from pydantic import BaseModel
from app import ask

app = FastAPI()

class Question(BaseModel):
    question: str

@app.get("/")
def root():
    return {"message": "CollegeBot API is running!"}

@app.post("/ask")
def ask_question(q: Question):
    answer = ask(q.question)
    return {"question": q.question, "answer": answer}