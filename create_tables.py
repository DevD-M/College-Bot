
from database import engine, Base
from models import User, Conversation, Message, Feedback

Base.metadata.create_all(bind=engine)
print("Tables created successfully")