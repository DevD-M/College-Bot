from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware 
from app import ask
from agent import app_graph  

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://campuscompass-bu.lovable.app"],  # tera exact frontend domain
    allow_credentials=True,  # yeh naya add karna hai — cookies allow karne ke liye
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

@app.post("/agent-ask")                          
def agent_ask_question(q: Question):
    result = app_graph.invoke({"messages": [("user", q.question)]})
    answer = result["messages"][-1].content
    return {"question": q.question, "answer": answer}