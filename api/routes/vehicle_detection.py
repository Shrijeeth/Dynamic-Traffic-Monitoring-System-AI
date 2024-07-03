"""
Vehicle Detection Controller
"""

from fastapi import APIRouter, UploadFile

from src.services.vehicle_detection.vehicle_detection_service import detect_vehicles


router = APIRouter()


@router.post("/detect-vehicles")
async def detect_vehicles_controller(files: list[UploadFile]) -> dict:
    """
    This function is the controller for the vehicle detection endpoint.
    It receives a list of images as UploadFile and calls the detect_vehicles function
    from the vehicle detection service to detect vehicles from given images.
    The result is then returned as a dictionary.

    Args:
        files (list[UploadFile]): A list of images to be processed.

    Returns:
        dict: A dictionary containing the result of the vehicle detection.
    """
    # Call the detect_vehicles function from the vehicle detection service
    result = await detect_vehicles(files)

    # Return the result as a dictionary
    return {"data": result}
