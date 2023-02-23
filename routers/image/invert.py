from fastapi import APIRouter, Query, Response
from main import util
from PIL import ImageOps

router = APIRouter(prefix="/image", tags=["File"])
    
@router.get("/invert",
    response_class=Response,
    status_code=200,
    description="Make an invert filter using your own image",
    responses=util.responses(image=True)
)
async def invert(
    image: str = Query(description="The image url to invert"),
    width: int | float | None = Query(None, description="The width size dimensions", ge=15, le=2048),
    height: int | float | None = Query(None, description="The height size dimensions", ge=15, le=2048)
    ):
    image = await util.load_image(image, param="image")
    f = ImageOps.invert(image.convert('RGB'))

    return Response(content=util.render(f.resize((width or image.width, height or image.height))).getvalue(), media_type="image/png")