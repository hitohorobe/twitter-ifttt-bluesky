import os
from logging import getLogger

from fastapi import FastAPI

from app.router import root_api_router

env = os.getenv("ENV", "local")
logger = getLogger("uvicorn.app")

if env == "local":
    app = FastAPI()
    app.include_router(root_api_router)

else:
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
    app.include_router(root_api_router)
