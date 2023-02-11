from fastapi import FastAPI
import importlib.util, importlib, os

class Util:
    def __init__(self, app: FastAPI):
        self.app = app

    def read(self) -> None:
        for folder in os.listdir("./routers"):
            for file in os.listdir(f"./routers/{folder}"):
                if file.endswith(".py"):
                    name = self.__resolve_name__(file[:-3])
                    r = importlib.import_module(f"routers.{folder}.{name}", None)
                    if hasattr(r, "router"):
                        self.app.include_router(getattr(r, "router"))

    def __resolve_name__(self, name: str) -> str:
        return importlib.util.resolve_name(name, None)