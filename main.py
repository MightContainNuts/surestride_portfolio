from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from pydantic import BaseModel

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


messages = []
user_handlers = {}


class Message(BaseModel):
    sender: str
    message: str

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/about", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/certificates", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("certificates.html", {"request": request})

@app.get("/web_tech_stack", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("web_tech_stack.html", {"request": request})

@app.get("/chat", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.get("/legal_stuff", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("legal_stuff.html", {"request": request})


@app.post("/chat/send_message")
def send_message(user_msg: Message, request: Request):
    if not user_msg.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    print(f"✌🏻 Message received: {user_msg.message}")
    messages.append(user_msg)

    ai_msg = Message(sender="🤖", message="This is a dummy response from the AI. #TODO ")

    print(f"📩 {ai_msg}")
    messages.append(ai_msg)

    # Return status and updated messages
    return {"status": "success", "messages": messages}


@app.get("/chat/get_messages", response_class=JSONResponse)
def get_messages():
    return {"messages": messages}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)

