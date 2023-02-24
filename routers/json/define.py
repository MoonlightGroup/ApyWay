from fastapi import APIRouter, Query
from fastapi.exceptions import HTTPException
from core.schemas import HTTPResponse
from main import util

router = APIRouter(prefix="/json", tags=["JSON"])

@router.get("/define",
    response_model=HTTPResponse,
    description="Define a term using the urban dictionary",
    responses=util.responses()
)
async def define(
        query: str = Query(description="The term to define", min_length=2),
        limit: int = Query(5, description="The limit of elements to display", ge=1, le=10)
    ):
    r = await util.request(url="https://api.urbandictionary.com/v0/define", params={"term": query})
    if not r or not r["list"]:
        raise HTTPException(404, detail={"error": "Your query was not found", "loc": "query", "param_type": "query"})
    return HTTPResponse.use(status=200, data=r["list"][0:limit])