from fastapi import APIRouter

from app.controllers import health_controller, twitter_to_bluesky_controller

root_api_router = APIRouter()
root_api_router.include_router(health_controller.router, tags=["health"])
root_api_router.include_router(twitter_to_bluesky_controller.router, tags=["twitter_to_bluesky"])