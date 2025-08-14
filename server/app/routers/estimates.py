from fastapi import APIRouter

router = APIRouter()

@router.post("/estimates")
async def find_estimates(data: dict):
    return ""