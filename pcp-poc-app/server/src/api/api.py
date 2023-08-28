from fastapi import APIRouter
from .router import default, sres_endpoints, system_mapping_endpoints, contact_tank_endpoints, audit_endpoints

api_router = APIRouter()
default_router = APIRouter(tags=["default"])

default_router.include_router(default.router)
api_router.include_router(sres_endpoints.router)
api_router.include_router(system_mapping_endpoints.router)
# api_router.include_router(contact_tank_endpoints.router)
# api_router.include_router(audit_endpoints.router)
