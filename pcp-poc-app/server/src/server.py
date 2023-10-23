from api.api import api_router, default_router
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from core.auth import get_cached_token, get_user_impersonation_token

api = FastAPI(title="Product Config Portal API Server", debug=True)

def get_token():
    """dependency function to get the AAD token"""
    # token = get_cached_token()
    token = get_user_impersonation_token()
    if not token:
        raise ValueError("Invalid AAD Token")
    return token


def initialize_fastapi_backend():
    """Initialises our fastapi server"""
    api.mount("/static", StaticFiles(directory="static"), name="static")
    api.include_router(default_router, tags=["default"])
    api.include_router(api_router, tags=["api"])
    return api


api: FastAPI = initialize_fastapi_backend()


@api.on_event("startup")
def startup_event():
    api.state.token = get_token()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server:api", host="127.0.0.1", port=8000, reload=True)
