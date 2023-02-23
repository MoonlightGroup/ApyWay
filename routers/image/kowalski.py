from fastapi import APIRouter, Query, Response
from main import util
from PIL import Image, ImageDraw, ImageSequence
import io, textwrap

router = APIRouter(prefix="/image", tags=["File"])
    
@router.get("/kowalski",
    response_class=Response,
    status_code=200,
    description="",
    responses=util.responses(image=True)
)
async def kowalski(
        text: str = Query(description=""),
    ):
    text = textwrap.fill(text, 13)

    font = await util.load_font("https://github.com/thedemons/merge_color_emoji_font/blob/main/seguiemj.ttf?raw=true", 23)
    bg = Image.open("static/assets/images/kowalski.gif")
    frames = []

    for frame in ImageSequence.Iterator(bg):
        frame = frame.convert("RGBA")
        bg2 = Image.new("RGBA", bg.size)
        d = ImageDraw.Draw(bg2)
        d.text((280, 90), text[:100], fill="#000000", font=font)
        bg2 = bg2.rotate(11.5, resample=Image.BICUBIC)
        frame = Image.alpha_composite(frame, bg2)
        del d
        b = io.BytesIO()
        frame.save(b, format="GIF")
        frame = Image.open(b)
        b.seek(0)
        frames.append(frame)
    buff = io.BytesIO()
    frames[0].save(buff, save_all=True, append_images=frames[1:], disposal=2, format="GIF")
    buff.seek(0)

    return Response(content=buff.getvalue(), media_type="image/gif")