from fastapi import APIRouter
from .router import default, sres_endpoints

api_router = APIRouter()
default_router = APIRouter(tags=["default"])

default_router.include_router(default.router)
api_router.include_router(sres_endpoints.router)
