from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

app = FastAPI()
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

@app.get("/chat", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.get("/legal_stuff", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("legal_stuff.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)

