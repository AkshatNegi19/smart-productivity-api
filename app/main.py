from fastapi import FastAPI
from .routers import users, tasks, comments, analytics

app = FastAPI()

app.include_router(users)
app.include_router(tasks)
app.include_router(comments)
app.include_router(analytics)

@app.get("/")
def home():
    return {"message": "Smart Productivity API is Running!"}
