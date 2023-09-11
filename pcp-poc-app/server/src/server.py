from api.api import api_router, default_router
from core import config as config_manager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

api = FastAPI()


def initialize_fastapi_backend():
    # settings = config_manager.get_settings()
    api.mount("/static", StaticFiles(directory="static"), name="static")
    api.include_router(default_router, tags=["default"])
    api.include_router(api_router, tags=["api"])

    return api


api: FastAPI = initialize_fastapi_backend()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server:api", host="127.0.0.1", port=8000, reload=True)

