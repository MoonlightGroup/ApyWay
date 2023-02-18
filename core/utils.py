from traceback import format_exception
from fastapi import FastAPI, Response
from fastapi.exceptions import HTTPException
from typing import Any
from .schemas import HTTPBadResponse, HTTPResponse
from io import BytesIO
from PIL import Image
import importlib.util, importlib, os, aiohttp, pydash

class ImageResponse(Response):
    media_type = "image/png"

class Util:
    def __init__(self, app: FastAPI) -> None:
        self.app = app
        self.p = pydash

    def responses(self, image: bool = False, media="image/png", description="The final image") -> dict[int, Any]:
        return { 200: { "description": description, "content": { media: {} } } if image else { "model": HTTPResponse }, 422: { "model": HTTPBadResponse }, 400: { "model": HTTPBadResponse }, 404: { "model": HTTPBadResponse }, 500: { "model": HTTPBadResponse } }

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
    
    async def load_image(self, body: str, mode='RGBA', use ='url', param=None):
        if not body:
            if param:
                raise HTTPException(status_code=422, detail={ "error": "Invalid image URL provided", "loc": param, "param_type": "query" })
            else:
                return None
        if use.lower() == 'url':
            try:
                r = await self.request(url=body, like='read')
                with Image.open(BytesIO(r)) as inp:
                    return inp.convert(mode)
            except:
                if param:
                    raise HTTPException(status_code=422, detail={ "error": "Invalid image URL provided", "loc": param, "param_type": "query" })
                else:
                    return None
        elif use.lower() == 'path':
            try:
                with open(body, 'rb') as document:
                    return Image.open(BytesIO(document.read())).convert(mode)
            except:
                if param:
                    raise HTTPException(status_code=422, detail={ "error": "Invalid image URL provided", "loc": param, "param_type": "query" })
                else:
                    return None
    
    def render(self, img: Image.Image, format="PNG"):
        buff = BytesIO()
        img.save(buff, format)
        if format.lower() != "gif":
            buff.seek(0)
        else:
            buff.seek(0, 0)
        return buff
    
    def exception(self, ex: Exception):
        return "\n".join(format_exception(ex))