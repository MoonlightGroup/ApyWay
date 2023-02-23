from fastapi import APIRouter, Query, Response
from main import util

router = APIRouter(prefix="/image", tags=["File"])
    
@router.get("/circle",
    response_class=Response,
    status_code=200,
    description="",
    responses=util.responses(image=True)
)
async def circle(
        image: str = Query(description="The image url to transform"),
        width: int | float | None = Query(512, description="The width size dimensions", ge=15, le=2048),
        height: int | float | None = Query(512, description="The height size dimensions", ge=15, le=2048)
    ):
    image = (await util.load_image(image, param="image"))
    f = util.circle_image(image)

    return Response(content=util.render(f.resize((width or image.width, height or image.height))).getvalue(), media_type="image/png")