from fastapi import FastAPI, HTTPException, Depends, APIRouter, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
from pydantic import BaseModel
from app.routes.auth_router import router as auth_router
from app.routes.chat_router import router as chat_router
from app.db.models import User


app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your_secret_key")

app.include_router(auth_router, prefix="/auth")
app.include_router(chat_router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")





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


@app.get("/legal_stuff", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("legal_stuff.html", {"request": request})










if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)

