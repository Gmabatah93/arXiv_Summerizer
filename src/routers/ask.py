from fastapi import APIRouter

router = APIRouter()

@router.post("/ask")
def ask_question():
    return {"answer": "Mock response"}