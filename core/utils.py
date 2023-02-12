from traceback import format_exception
from fastapi import FastAPI
from .schemas import HTTPBadResponse, HTTPResponse
import importlib.util, importlib, os, aiohttp, pydash

class Util:
    def __init__(self, app: FastAPI):
        self.app = app
        self.responses = { 200: { "model": HTTPResponse }, 422: { "model": HTTPBadResponse }, 400: { "model": HTTPBadResponse }, 404: { "model": HTTPBadResponse }, 500: { "model": HTTPBadResponse } }
        self.p = pydash

    def read(self) -> None:
        for folder in os.listdir("./routers"):
            for file in os.listdir(f"./routers/{folder}"):
                if file.endswith(".py"):
                    name = self.__resolve_name__(file[:-3])
                    r = importlib.import_module(f"routers.{folder}.{name}", None)
                    if hasattr(r, "router"):
                        self.app.include_router(getattr(r, "router"))

    def __resolve_name__(self, name: str) -> str:
        return importlib.util.resolve_name(name, None)
    
    async def request(self, *, url: str, params: dict = {}, headers: dict = {}, like = "json"):
        try:
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.get(url=url, params=params) as r:
                    if r.status != 200 and r.status != 201:
                        return None
                    if like.lower() == 'json':
                        return await r.json()
                    elif like.lower() == 'text':
                        return await r.text()
                    elif like.lower() == 'read':
                        return await r.read()
                    else:
                        raise SyntaxError('Invalid like method provided in request')
        except:
            return None
    
    def exception(self, ex: Exception):
        return "\n".join(format_exception(ex))