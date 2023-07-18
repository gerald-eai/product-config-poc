from fastapi import APIRouter
from .router import default

api_router = APIRouter()
default_router = APIRouter(tags=["default"])

default_router.include_router(default.router)
