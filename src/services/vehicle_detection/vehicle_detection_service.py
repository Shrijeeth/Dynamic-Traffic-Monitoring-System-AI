"""
Vehicle Detection Service
"""

from typing import Optional
from fastapi import UploadFile

from worker import worker
from configs.config import get_settings
from src.model_registry.vehicle_detection.yolo_object_detection_model_registry import (
    YoloObjectDetectionModelRegistry,
)
from src.schemas.vehicle_detection import VehicleDetectionInput
from src.services.notification.notification_service import notify
from src.utils.notification.types import EmailTemplate
from src.utils.utils import run_in_process
from src.utils.vehicle_detection.constants import YOLOV8_VEHICLE_CLASSES
from src.utils.vehicle_detection.utils import (
    convert_files_to_numpy_arrays,
    get_results_from_yolo,
)


@worker.task(name="detect_vehicles")
async def detect_vehicles(images: list[dict], request: Optional[VehicleDetectionInput] = None) -> list:
    """
    Detect vehicles in a list of images.

    Args:
        images (list[UploadFile]): List of images to detect vehicles in.

    Returns:
        List of dictionaries containing information about the detected vehicles.
    """
    # Initialize the YoloV8 model registry
    model = YoloObjectDetectionModelRegistry()

    # Load the YoloV8 model
    model_obj = model.load_model()

    # Convert the images to numpy arrays and store them in a dictionary
    processed_images = await convert_files_to_numpy_arrays(images)
    # Convert the dictionary values to a list
    image_data = list(processed_images.values())

    # Predict on the image data using the YoloV8 model
    preds = await run_in_process(
        model_obj.predict, image_data, classes=YOLOV8_VEHICLE_CLASSES
    )

    # Create a dictionary to store the results
    results = {}

    # Iterate over the predictions and image file names
    for pred, image in zip(preds, processed_images.keys()):
        # Add the prediction to the result dictionary
        results[image] = pred

    # Create a list to store the results
    response = []

    # Iterate over the results and images
    for filename, result in results.items():
        # Find the image with the matching filename
        image = next((image for image in images if image.filename == filename), None)

        # If an image is found, append the result to the response list
        if image:
            # Get the results from the Yolo prediction
            response.append(
                get_results_from_yolo(result, image.filename, model_obj.names)
            )

    if request:
         notification_data = {
              "template": EmailTemplate.VEHICLE_DETECTION.value,
              "from_mail": get_settings().SMTP_USERNAME,
              "message": {"result": response},
              "to_mail": request.notification_addresses,
              "subject": "Vehicle Detection Results",
         }
         task = notify.delay(notification_data, request.notify_to.value)
         return {"data": {
              "task_id": task.id
         }}
    # Return the list of results
    return response
