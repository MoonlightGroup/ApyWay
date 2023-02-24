from fastapi import APIRouter, Query
from core.schemas import HTTPResponse
from calendar import month as MONTH
from datetime import datetime
from main import util

router = APIRouter(prefix="/json", tags=["JSON"])

@router.get("/calendar",
    response_model=HTTPResponse,
    description="See a month calendar",
    responses=util.responses()
)
async def calendar(
        year: int = Query(2023, le=3000, ge=1000, description="The year calendar"),
        month: int = Query(datetime.now().month, le=12, ge=1, description="The month calendar")
    ):
    return HTTPResponse.use(status=200, data=MONTH(year, month))