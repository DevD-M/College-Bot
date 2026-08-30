from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware 
from app import ask
from agent import app_graph  
from auth_routes import router as auth_router
from conversation_routes import router as conversation_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(conversation_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://campuscompass-bu.lovable.app"], 
    allow_credentials=True,  
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