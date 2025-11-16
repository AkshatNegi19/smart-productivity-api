from fastapi import APIRouter

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/overview")
def analytics_overview():
    return {"message": "Analytics overview will come here"}
