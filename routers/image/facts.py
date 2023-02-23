from fastapi import APIRouter, Query, Response
from main import util
from PIL import Image
import textwrap

router = APIRouter(prefix="/image", tags=["File"])
    
@router.get("/facts",
    response_class=Response,
    status_code=200,
    description="",
    responses=util.responses(image=True)
)
async def facts(
        text: str = Query(description=""),
    ):
    text = textwrap.fill(text, 22)
    font = await util.load_font("https://github.com/thedemons/merge_color_emoji_font/blob/main/seguiemj.ttf?raw=true", 23)
    
    bg = await util.load_image("static/assets/images/facts.jpeg", use="path")
    base = Image.new("RGBA", bg.size, (0, 0, 0, 0))
    base.paste(bg.resize(bg.size), (0, 0), bg.resize(bg.size))
    
    base = await util.draw_text(base, (75, 400), text, font=font, colour="black", rotation=-15)

    return Response(content=util.render(base).getvalue(), media_type="image/png")