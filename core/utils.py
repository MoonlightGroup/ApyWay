from traceback import format_exception
from fastapi import FastAPI, Response
from fastapi.exceptions import HTTPException
from typing import Any
from .schemas import HTTPBadResponse, HTTPResponse
from io import BytesIO
from PIL import Image, ImageFont, ImageDraw, ImageFont
from pilmoji_fixed import AsyncPilmoji
import importlib.util, importlib, os, aiohttp, pydash, re

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
                return None

    async def load_font(self, url: str, size: int):
        r = await self.request(url=url, like='read')
        buff = BytesIO(r)
        return ImageFont.truetype(buff, size, layout_engine=ImageFont.LAYOUT_RAQM)

    def render(self, img: Image.Image, format="PNG"):
        buff = BytesIO()
        img.save(buff, format)
        if format.lower() != "gif":
            buff.seek(0)
        else:
            buff.seek(0, 0)
        return buff

    def is_hex(self, text):
        try:
            return True if re.match('^([A-F0-9]{6}|[A-F0-9]{3})$', text, flags=re.IGNORECASE) else False
        except:
            return None

    def circle_image(self, img):
        bigsize = (img.size[0] * 3, img.size[1] * 3)
        mask = Image.new("L", bigsize, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(img.size, Image.ANTIALIAS)
        img.putalpha(mask)
        return img

    async def draw_text_emoji(self, img, position, text, font=None, align='left', colour="Black", stroke_fill="Black", stroke_width=0, rotation=0, anchor=None, scale=1.15, pos=(0, -2)):
        x, y = position
        if font is None:
           font = ImageFont.load_default()
        a = Image.new("RGBA", img.size, (255, 255, 255, 0))
        ImageDraw.Draw(a).text((x, y), text, font=font, fill=colour, align=align, stroke_fill=stroke_fill, stroke_width=stroke_width, anchor=anchor, embedded_color=True)
        a = a.rotate(rotation, resample=Image.BICUBIC)
        return Image.alpha_composite(img, a)
    
    async def draw_text(self, img, position, text, font=None, align='left', colour=1, stroke_fill="Black", stroke_width=0, rotation=0, anchor=None, scale=1.15, pos=(0, -2)):
        x, y = position
        if font is None:
            font = ImageFont.load_default()
        a = Image.new("RGBA", img.size, (255, 255, 255, 0))
        async with AsyncPilmoji(a) as pilmoji:
            await pilmoji.text((x, y), text, font=font, fill=colour, align=align, stroke_fill=stroke_fill, stroke_width=stroke_width, anchor=anchor, emoji_size_factor=scale, emoji_position_offset=pos)
        a = a.rotate(rotation, resample=Image.BICUBIC)
        return Image.alpha_composite(img, a)

    def exception(self, ex: Exception):
        return "\n".join(format_exception(ex))