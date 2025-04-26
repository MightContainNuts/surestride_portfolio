from fastapi import APIRouter, HTTPException, status, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlmodel import select
from app.db.db_init import DBHandler
from app.db.models import User
import bcrypt


auth_routes = APIRouter()

# Setup Jinja2 Templates
templates = Jinja2Templates(directory="app/templates")

# Pydantic Models
class UserIn(BaseModel):
    username: str
    password: str
    email: str

class UserOut(BaseModel):
    username: str
    email: str

class Login(BaseModel):
    username: str
    password: str

# Render the auth.html page
@auth_routes.get("/auth", response_class=HTMLResponse)
def auth_page(request: Request):
    return templates.TemplateResponse("auth.html", {"request": request})

# Handle registration
@auth_routes.post("/register", response_model=UserOut)
def register(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    email: str = Form(...),
):
    # Check if the username already exists
    with DBHandler() as db:
        existing_user = db.session.exec(select(User).where(User.username == username)).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )

        # Hash the password
        hashed_password = User.hash_password(password)
        print(f"Hashed password: {hashed_password}")

        # Add and commit to the database
        db.add_user(username, email, hashed_password)


        print(f"User {username} registered successfully!")
        request.session["message"] = "User added. Please log in."

    return RedirectResponse(url="/chat", status_code=303)

# Handle login
@auth_routes.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    with DBHandler() as db:
        user = db.get_user_by_username(username)
        if not user:
            request.session["message"] = "Invalid credentials"
            print(f"Invalid credentials for user {username}")
            return RedirectResponse(url="/auth/auth", status_code=303)
        print(f"User fetched: {user}")
        is_valid_password = bcrypt.checkpw(password.encode('utf-8'), user.hashed_password.encode('utf-8'))
    if not user or not is_valid_password:
        request.session["message"] = "Invalid credentials"
        print(f"Invalid credentials for user {username}")
        return RedirectResponse(url="/auth/auth", status_code=303)

    request.session["user_id"] = user.user_id
    return RedirectResponse(url="/chat", status_code=303)

@auth_routes.get("/logout")
async def logout(request: Request):
    request.session.clear()  # Clear session
    return RedirectResponse(url="/", status_code=303)