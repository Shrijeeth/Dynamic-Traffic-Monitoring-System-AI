"""
Vehicle Detection Controller
"""

from typing import Optional
from fastapi import APIRouter, Depends, UploadFile

from configs.config import get_settings
from src.schemas.vehicle_detection import VehicleDetectionInput
from src.services.notification.notification_service import notify
from src.services.vehicle_detection.vehicle_detection_service import detect_vehicles
from src.utils.notification.types import EmailTemplate


router = APIRouter()


@router.post("/detect-vehicles")
async def detect_vehicles_controller(
    files: list[UploadFile], request: Optional[VehicleDetectionInput] = Depends(VehicleDetectionInput)
) -> dict:
    """
    This function is the controller for the vehicle detection endpoint.

    It receives a list of images as UploadFile and calls the
    detect_vehicles function from the vehicle detection service to detect
    vehicles from given images. The result is then returned as a dictionary.

    Args:
        request (VehicleDetectionInput): A request object containing a list of
            images to be processed and a notification destination.

    Returns:
        dict: A dictionary containing the result of the vehicle detection.
    """
    # Call the detect_vehicles function from the vehicle detection service
    # using the list of files from the request
    if request:
         result = await detect_vehicles.delay(files, request)
    else:
        result = await detect_vehicles.delay(files, request)
    # Return the result as a dictionary
    return {"data": result}
