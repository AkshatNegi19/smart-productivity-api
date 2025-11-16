from fastapi import APIRouter, HTTPException
from app.models import User, Login
from app.database import users
from passlib.context import CryptContext
from app.auth import create_token

router = APIRouter(prefix="/users", tags=["User"])

# Use argon2 instead of bcrypt
pwd = CryptContext(schemes=["argon2"], deprecated="auto")

@router.post("/register")
def register(data: User):
    if users.find_one({"email": data.email}):
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed = pwd.hash(data.password)  # no 72-char limit with argon2
    user = {"name": data.name, "email": data.email, "password": hashed}

    users.insert_one(user)
    return {"message": "User created successfully"}

@router.post("/login")
def login(data: Login):
    user = users.find_one({"email": data.email})
    if not user or not pwd.verify(data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({"user_id": str(user["_id"])})
    return {"access_token": token}
