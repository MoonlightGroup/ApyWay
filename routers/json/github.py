from fastapi import APIRouter, Query
from fastapi.exceptions import HTTPException
from core.schemas import HTTPResponse
from typing import Literal
from main import util

router = APIRouter(prefix="/json", tags=["JSON"])

@router.get("/github",
response_model=HTTPResponse,
description="Get information about a github repository/user",
responses=util.responses
)
async def github(
    query: str = Query(description="The repo/user to search in github", min_length=2),
    type: Literal["user", "User", "repo", "Repo", "USER", "REPO"] = Query("repo", description="The search type to do")
    ):
    if type.lower() == "repo":
        url = f"https://api.github.com/search/repositories?q={query}&page=1&per_page=1"
        res = await util.request(url=url)
        if not res or not util.p.get(res, "items[0]"):
            raise HTTPException(status_code=404, detail="Your query was not found")
        return HTTPResponse.use(status=200, data=res["items"][0])
    elif type.lower() == "user":
        url = f"https://api.github.com/users/{query}"
        res = await util.request(url=url)
        if not res or not util.p.get(res, "login"):
            raise HTTPException(status_code=404, detail="Your query was not found")
        return HTTPResponse.use(status=200, data=res)