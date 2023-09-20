from cachetools import TTLCache
from fastapi import FastAPI, APIRouter
from typing import List


# on app startup, connect to msal, load the token and store it in the cache
class ProductConfigAPI(FastAPI):
    def init(self):
        cache = TTLCache(maxsize=1, ttl=3600)

    # include a function that adds in all of the API routes
    def init_api_routers(self, routers: List[APIRouter]):
        for route in routers:
            self.include_router(route)
