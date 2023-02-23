from fastapi import APIRouter, Query, Response
from main import util
from PIL import Image, ImageDraw
from fastapi.exceptions import HTTPException

router = APIRouter(prefix="/image", tags=["File"])

def i2h(nr):
  h = format(int(nr), 'x')
  return '0' + h if len(h) % 2 else h
    
@router.get("/color",
    response_class=Response,
    status_code=200,
    description="Make an image using your color code",
    responses=util.responses(image=True)
)
async def color(
        code: str = Query(description="The hexadecimal color code"),
        width: int | float | None = Query(512, description="The width size dimensions"),
        height: int | float | None = Query(512, description="The height size dimensions")
    ):
    if not util.is_hex(color):
        raise HTTPException(422, detail={"error": "Invalid Hexadecimal code provided", "loc": "color", "param_type": "query"})
    bg = Image.new("RGBA", (512, 512))
    base = Image.new("RGBA", bg.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(base, "RGBA")
    draw.rounded_rectangle((0, 0, 512, 512), 55, fill=f"#{code}")
    font = await util.load_font("https://github.com/jabes/terrace/blob/master/Terrace/resources/fonts/VCR-OSD-Mono.ttf?raw=true", 60)
    draw.text((11, 420), f"#{code}", font=font, fill="#ffff", align="left")
    base.rotate(0, resample=Image.BICUBIC)
    f = Image.alpha_composite(bg, base).resize((width, height))

    return Response(content=util.render(f).getvalue(), media_type="image/png")