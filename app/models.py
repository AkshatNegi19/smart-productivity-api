from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    name: str
    email: EmailStr
    password: str

class Login(BaseModel):
    email: EmailStr
    password: str

class Task(BaseModel):
    title: str
    description: str
    category: Optional[str] = None

class UpdateTask(BaseModel):
    title: Optional[str]
    description: Optional[str]
    completed: Optional[bool]
    category: Optional[str]
