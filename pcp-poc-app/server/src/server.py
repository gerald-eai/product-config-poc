from fastapi import FastAPI
from fastapi import APIRouter
from api.api import default_router
from fastapi.staticfiles import StaticFiles

api = FastAPI()


def initialize_fastapi_backend():
    api.mount("/static", StaticFiles(directory="static"), name="static")
    api.include_router(default_router, tags=["default"])

    return api


api: FastAPI = initialize_fastapi_backend()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server:api", host="0.0.0.0", port=8000, reload=True)
