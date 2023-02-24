from deep_translator import GoogleTranslator
from fastapi import APIRouter, Query
from fastapi.exceptions import HTTPException
from core.schemas import HTTPResponse
from main import util

router = APIRouter(prefix="/json", tags=["JSON"])

def load_lang(idiom: str):
    if not idiom:
        return None
    return idiom.lower().replace("zh-cn", "zh-CN").replace("zh-tw", "zh-TW").replace("ch", "zh-CN")

@router.get("/translate",
    response_model=HTTPResponse,
    description="Translate a text using the target idiom abbreviation",
    responses=util.responses()
)
async def translator(
        text: str = Query(description="The text to translate", min_length=2, max_length=2500),
        to: str = Query(description="The target idiom"),
        _from: str = Query("auto", title="from", description="An optional source idiom abbreviation. Default is auto")
    ):
    to = load_lang(to)
    _from = load_lang(_from)
    CLASS = GoogleTranslator(source="auto", target="en")
    LANGUAGES = list(CLASS.get_supported_languages(as_dict=True).values())
    if to not in LANGUAGES or _from not in LANGUAGES and _from != "auto":
        raise HTTPException(status_code=400, detail={ "error": "The provided language is not supported", "metadata": { "allowed": LANGUAGES }, "loc": "to" if to not in LANGUAGES else "from", "param_type": "query" })
    CLASS.target = to
    CLASS.source = _from
    result = CLASS.translate(text)
    if not result:
        raise HTTPException(status_code=400, detail={ "error": "Your translation is invalid because no server response", "loc": None, "param_type": "query" })
    return HTTPResponse.use(status=200, data=result)