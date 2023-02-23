from fastapi import APIRouter, Query, Response
from main import util
from PIL import Image, ImageDraw

router = APIRouter(prefix="/image", tags=["File"])
    
@router.get("/supreme",
    response_class=Response,
    status_code=200,
    description="Makes your own supreme logo",
    responses=util.responses(image=True)
)
async def supreme(
        text: str = Query(description="The text that will be drawn on the logo", max_length=50),
    ):
    font = await util.load_font("https://github.com/kukai-wallet/experimental/blob/master/HelveticaNowText-ExtBdIta.ttf?raw=true", 70)
    s = font.getsize(text)

    base = Image.new("RGBA", (s[0] + 40, 104))
    base2 = Image.new("RGBA", base.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(base2, "RGBA")

    draw.rounded_rectangle((0, 0, base.width, base.height), 10, fill="Red")
    draw.text((16, 14), f"{text[0:50]}", font=font, fill="White", align="left")
    f = Image.alpha_composite(base, base2)

    return Response(content=util.render(f).getvalue(), media_type="image/png")