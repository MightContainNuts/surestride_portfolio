from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request



templates = Jinja2Templates(directory="app/templates")
public_routes= APIRouter()


@public_routes.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@public_routes.get("/about", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@public_routes.get("/certificates", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("certificates.html", {"request": request})

@public_routes.get("/web_tech_stack", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("web_tech_stack.html", {"request": request})


@public_routes.get("/legal_stuff", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("legal_stuff.html", {"request": request})