import uvicorn, json, logging, warnings
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.staticfiles import StaticFiles
from core.utils import Util
from core.schemas import HTTPBadResponse

warnings.filterwarnings('ignore')

app = FastAPI(
    title="APY",
    debug=False,
    description="A powerful rest API written in Python with cool routes",
    version="0.0.1",
    docs_url=None,
    redoc_url=None
)

util = Util(app)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/launcher", include_in_schema=False)
async def custom_swagger_ui_html_github():
    return get_swagger_ui_html(
    openapi_url=app.openapi_url,
    title=f"{app.title} - Launcher & Documentation",
    # swagger_ui_dark.css raw url
    swagger_css_url="/static/style.css"
    )

@app.get("/docs", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Documentation",
        redoc_js_url="https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js",
    )

@app.exception_handler(422)
@app.exception_handler(RequestValidationError)
async def validation_error(request, exc: RequestValidationError | HTTPException):
    d = json.loads(exc.json())[0] if hasattr(exc, "json") else exc.detail
    param, loc = d.get("loc", [None, None])
    return HTTPBadResponse.use(status=exc.status_code if hasattr(exc, "status_code") else 422, data={ "error": d.get("msg", "Unknown error").title(), "loc": loc, "param_type": param })

@app.exception_handler(400)
@app.exception_handler(404)
async def bad_request_error(request, exc: HTTPException):
    return HTTPBadResponse.use(status=exc.status_code, data=exc.detail)

@app.exception_handler(500)
async def internal_error(request, exc):
    return HTTPBadResponse.use(status=500, data={ "error": "Internal server error", "loc": None, "param_type": None })

@app.on_event("startup")
async def startup_event():
    print("API is ready")
    util.read()

uvicorn.Config(app, log_level=logging.ERROR)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=False)