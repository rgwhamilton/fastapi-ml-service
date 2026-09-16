
from fastapi import APIRouter
router = APIRouter()
@router.get(
    "/health",
    summary="Application Health Check",
    tags=["Health"]
)
def health():
    return {
        "status": "healthy"
    }
