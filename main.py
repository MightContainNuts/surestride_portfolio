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
    # You can pass variables to your template here
    return templates.TemplateResponse("index.html", {"request": request, "name": "FastAPI"})

@app.get("/about", response_class=HTMLResponse)
async def read_root(request: Request):
    # You can pass variables to your template here
    return templates.TemplateResponse("about.html", {"request": request, "name": "FastAPI"})

@app.get("/certificates", response_class=HTMLResponse)
async def read_root(request: Request):
    # You can pass variables to your template here
    return templates.TemplateResponse("certificates.html", {"request": request, "name": "FastAPI"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)

