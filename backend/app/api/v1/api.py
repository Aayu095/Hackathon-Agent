"""
API v1 router - Main API endpoints
"""

from fastapi import APIRouter
from app.api.v1.endpoints import chat, search, github, health, webhook

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(
    health.router,
    prefix="/health",
    tags=["health"]
)

api_router.include_router(
    chat.router,
    prefix="/chat",
    tags=["chat"]
)

api_router.include_router(
    search.router,
    prefix="/search",
    tags=["search"]
)

api_router.include_router(
    github.router,
    prefix="/github",
    tags=["github"]
)

api_router.include_router(
    webhook.router,
    prefix="/webhook",
    tags=["webhook"]
)
