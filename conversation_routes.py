# conversation_routes.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import User, Conversation, Message, Feedback
from schemas import ConversationResponse, MessageResponse, MessageCreate, FeedbackCreate
from dependencies import get_current_user
from agent import app_graph  # tera existing LangGraph agent

router = APIRouter(prefix="/conversations", tags=["conversations"])


@router.post("", response_model=ConversationResponse)
def create_conversation(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_conv = Conversation(user_id=current_user.id)
    db.add(new_conv)
    db.commit()
    db.refresh(new_conv)
    return new_conv


@router.get("", response_model=List[ConversationResponse])
def list_conversations(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    conversations = db.query(Conversation).filter(Conversation.user_id == current_user.id).all()
    return conversations


@router.get("/{conversation_id}", response_model=ConversationResponse)
def get_conversation(conversation_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()

    if conversation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")

    return conversation


@router.post("/{conversation_id}/messages", response_model=MessageResponse)
def send_message(
    conversation_id: int,
    message_data: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()

    if conversation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")

    try:
        user_message = Message(conversation_id=conversation_id, role="user", content=message_data.content)
        db.add(user_message)
        # NOTE: commit() abhi nahi kiya

        result = app_graph.invoke({"messages": [("user", message_data.content)]})
        bot_reply = result["messages"][-1].content

        bot_message = Message(conversation_id=conversation_id, role="bot", content=bot_reply)
        db.add(bot_message)

        db.commit()   # <-- SIRF YAHA, dono successful hone ke baad, ek hi commit
        db.refresh(bot_message)

    except Exception as e:
        db.rollback()   # <-- agar kahi bhi beech mein fail hua, sab undo
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to process message")

    return bot_message


@router.post("/messages/{message_id}/feedback")
def give_feedback(
    message_id: int,
    feedback_data: FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    message = db.query(Message).join(Conversation).filter(
        Message.id == message_id,
        Conversation.user_id == current_user.id
    ).first()

    if message is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")

    new_feedback = Feedback(
        message_id=message_id,
        rating=feedback_data.rating,
        comment=feedback_data.comment,
    )
    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)

    return {"message": "Feedback recorded", "feedback_id": new_feedback.id}