from fastapi import APIRouter, Query
from fastapi.exceptions import HTTPException
from core.schemas import HTTPResponse
from main import util

router = APIRouter(prefix="/json", tags=["JSON"])

@router.get("/npm",
    response_model=HTTPResponse,
    description="Fetch a package information from npmjs.com",
    responses=util.responses()
)
async def npm(
        query: str = Query(description="The package to fetch (exact match)", min_length=2)
    ):
    r = await util.request(url=f"https://registry.npmjs.org/{query.lower().replace(' ', '-')}")
    if not r:
        raise HTTPException(404, detail={"error": "Your query was not found", "loc": "query", "param_type": "query"})
    return HTTPResponse.use(status=200, data=r)