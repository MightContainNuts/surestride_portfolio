from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from app.db.models import User

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

messages = []
user_handlers = {}


class Message(BaseModel):
    sender: str
    message: str

    def __str__(self):
        return f"{self.sender}: {self.message}"


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


@router.get("/chat", response_class=HTMLResponse)
async def chat(request: Request, current_user: User = Depends(ensure_authenticated_user)):
    return templates.TemplateResponse("chat.html", {"request": request, "user": current_user})


@router.get("/chat/get_messages", response_class=JSONResponse)
def get_messages():
    return {"messages": messages}


@router.post("/chat/send_message")
def send_message(user_msg: Message, request: Request):
    if not user_msg.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    print(f"✌🏻 Message received: {user_msg.message}")
    messages.append(user_msg)

    ai_msg = Message(sender="🤖", message="This is a dummy response from the AI. #TODO ")

    print(f"📩 {ai_msg}")
    messages.append(ai_msg)

    return {"status": "success", "messages": messages}