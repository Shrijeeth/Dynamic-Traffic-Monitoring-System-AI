"""
Module to handle the API routes
"""

from fastapi import APIRouter

from api.routes import home, vehicle_detection

api_router = APIRouter()

api_router.include_router(home.router, tags=["Home"])
api_router.include_router(
    vehicle_detection.router, prefix="/vehicle-detection", tags=["Vehicle Detection"]
)
