from fastapi import APIRouter, Query
from fastapi.exceptions import HTTPException
from core.schemas import HTTPResponse
from main import util
import re

router = APIRouter(prefix="/json", tags=["JSON"])

@router.get("/imagesearch",
response_model=HTTPResponse,
description="Search images in bing.com",
responses=util.responses
)
async def image_search(
    query: str = Query(description="The query to search in the bing images", min_length=2)
    ):
    res = await util.request(url=f"https://www.bing.com/images/async?q={query}&adlt=on", like="read")
    if not res:
        raise HTTPException(404, detail={"error": "Your query was not found", "loc": "query", "param_type": "query"})
    links = re.findall("murl&quot;:&quot;(.*?)&quot;", res.decode("utf8"))
    return HTTPResponse.use(status=200, data=list(links))