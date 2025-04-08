from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from app.db.models import User

from app.services.chatbot import LangChainHandler
import markdown


chat_routes = APIRouter()

templates = Jinja2Templates(directory="app/templates")

messages = []
user_handlers = {}

chatbot = LangChainHandler()





class Message(BaseModel):
    sender: str
    message: str

    def __str__(self):
        return f"{self.sender}: {self.message}"

def convert_markdown_to_html(markdown_text: str) -> str:
    return markdown.markdown(markdown_text)

# Refactor this function to use session-based user check
async def ensure_authenticated_user(request: Request):
    print(f"🔒 Checking authentication for {request.client}")

    # Fetch user from the session (ensure 'user_id' is being stored correctly)
    user = request.session.get("user_id")
    if not user:
        print("❌ User not authenticated! Redirecting...")

        # Raising HTTPException for a 303 redirect
        raise HTTPException(
            status_code=303,  # 303 is used for redirection
            detail="Redirecting to login",
            headers={"Location": "/auth/auth"}  # Specify the redirection URL
        )

    print("✅ User authenticated!")
    return user


@chat_routes.get("/chat", response_class=HTMLResponse)
async def chat(request: Request, current_user: User = Depends(ensure_authenticated_user)):
    return templates.TemplateResponse("chat.html", {"request": request, "user": current_user})


@chat_routes.get("/chat/get_messages", response_class=JSONResponse)
def get_messages():
    # Return all messages (including AI and user messages)
    converted_messages = [
        {"sender": msg.sender, "message": convert_markdown_to_html(msg.message)}
        for msg in messages
    ]
    return {"messages": converted_messages}


@chat_routes.post("/chat/send_message")
def send_message(user_msg: Message, request: Request):
    if not user_msg.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    print(f"✌🏻 Message received: {user_msg.message}")
    messages.append(user_msg)

    # Simulate AI response using LangChain
    try:
        ai_response = chatbot.handle_message(user_msg.message)
        ai_msg = Message(sender="🤖", message=ai_response)
    except Exception as e:
        print(f"Error processing message: {e}")
        ai_msg = Message(sender="🤖", message="Sorry, I encountered an error processing your message.")

    print(f"📩 {ai_msg}")
    messages.append(ai_msg)

    return {"status": "success", "messages": [{"sender": msg.sender, "message": msg.message} for msg in messages]}