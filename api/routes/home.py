"""
Home Controller
"""

from fastapi import APIRouter


router = APIRouter()


@router.get("/")
def home() -> dict:
    """
    This function returns a welcome message to the user.

    Returns:
        dict: A dictionary containing the success status and message.
    """
    return {
        "success": True,
        "message": "Welcome to Dynamic Vehicle Monitoring System",
    }
