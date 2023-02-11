from fastapi import APIRouter
#fro

router = APIRouter(prefix="/json", tags=["JSON"])

@router.get("/test")
async def bla_bla(a: str = "Default"):
    return { "ma": a }