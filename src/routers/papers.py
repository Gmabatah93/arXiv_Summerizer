from fastapi import APIRouter

router = APIRouter(prefix="/papers", tags=["papers"])

@router.get("/")
def list_papers():
    return {"papers": [], "total": 0}