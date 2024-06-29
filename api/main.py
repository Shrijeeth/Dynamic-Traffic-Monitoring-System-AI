"""
Module to handle the API routes
"""

from fastapi import APIRouter

from api.routes import home

api_router = APIRouter()

api_router.include_router(home.router, tags=["Home"])
