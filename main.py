from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from app.routes import (
    auth_routes,
    chat_routes,
    public_routes
)


app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your_secret_key")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


app.include_router(auth_routes, prefix="/auth")
app.include_router(chat_routes)
app.include_router(public_routes)
















if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)

