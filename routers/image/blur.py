from fastapi import APIRouter, Query, Response
from main import util
from PIL import Image, ImageFilter

router = APIRouter(prefix="/image", tags=["File"])

@router.get("/blur",
    response_class=Response,
    status_code=200,
    description="Apply a blur filter to your own image",
    responses=util.responses(image=True)
)
async def blur(
        image: str = Query(description="The image URL"),
        amount: int | float | None = Query(5, description="The blur amount to apply to the image", ge=1, le=100)
    ):
    image = await util.load_image(image, param="image")
    base = Image.new("RGBA", image.size, (0, 0, 0, 0))
    base.paste(image, (0, 0), image)
    f = base.filter(ImageFilter.GaussianBlur(amount))

    return Response(content=util.render(f).getvalue(), media_type="image/png")