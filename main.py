import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from core.utils import Util

app = FastAPI(
    title="ApyWay",
    debug=False,
    description="A cool API for you!",
    version="0.0.1"
)
util = Util(app)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

util.read()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=False)