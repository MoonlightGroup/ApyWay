from fastapi import APIRouter

router = APIRouter(prefix="/json", tags=["JSON"])

@router.get("/uwu", description="Do something")
async def test():
    return { "ma": "uwu" }