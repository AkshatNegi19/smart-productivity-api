from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from app.auth import verify_token
from app.database import tasks
from app.models import Task, UpdateTask
from bson import ObjectId
import os

router = APIRouter(prefix="/tasks", tags=["Tasks"])
    
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_user(token: str):
    user = verify_token(token)
    if not user:
        raise HTTPException(401, "Invalid or expired token")
    return user["user_id"]

@router.post("/")
def create_task(data: Task, token: str = Depends(get_user)):
    task = {
        "title": data.title,
        "description": data.description,
        "category": data.category,
        "completed": False,
        "user_id": token,
        "attachment": None
    }
    tasks.insert_one(task)
    return {"message": "Task created"}

@router.get("/")
def get_tasks(token: str = Depends(get_user)):
    user_tasks = tasks.find({"user_id": token})
    return [{"id": str(t["_id"]), **t} for t in user_tasks]

@router.put("/{task_id}")
def update_task(task_id: str, data: UpdateTask, token: str = Depends(get_user)):
    updated = tasks.update_one(
        {"_id": ObjectId(task_id), "user_id": token},
        {"$set": {k: v for k, v in data.dict().items() if v is not None}}
    )

    if updated.matched_count == 0:
        raise HTTPException(404, "Task not found")
    return {"message": "Updated successfully"}

@router.delete("/{task_id}")
def delete_task(task_id: str, token: str = Depends(get_user)):
    tasks.delete_one({"_id": ObjectId(task_id), "user_id": token})
    return {"message": "Task deleted"}

@router.post("/{task_id}/upload")
def upload_file(task_id: str, file: UploadFile = File(...), token: str = Depends(get_user)):
    filename = f"{task_id}_{file.filename}"
    filepath = f"{UPLOAD_DIR}/{filename}"
    
    with open(filepath, "wb") as f:
        f.write(file.file.read())
    
    tasks.update_one({"_id": ObjectId(task_id)}, {"$set": {"attachment": filepath}})
    return {"message": "File uploaded"}
