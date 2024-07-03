"""
Vehicle Detection Service
"""

from fastapi import UploadFile

from src.model_registry.vehicle_detection.yolov8_model_registry import (
    YoloV8ModelRegistry,
)
from src.utils.utils import run_in_process
from src.utils.vehicle_detection.utils import (
    convert_files_to_numpy_arrays,
    get_results_from_yolo,
)


async def detect_vehicles(images: list[UploadFile]) -> list:
    """
    Detect vehicles in a list of images.

    Args:
        images (list[UploadFile]): List of images to detect vehicles in.

    Returns:
        List of dictionaries containing information about the detected vehicles.
    """
    # Initialize the YoloV8 model registry
    model = YoloV8ModelRegistry(version="l")

    # Load the YoloV8 model
    model_obj = model.load_model()

    # Convert the images to numpy arrays and store them in a dictionary
    processed_images = await convert_files_to_numpy_arrays(images)
    # Convert the dictionary values to a list
    image_data = list(processed_images.values())

    # Predict on the image data using the YoloV8 model
    preds = await run_in_process(model_obj.predict, image_data)

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
            response.append(get_results_from_yolo(result, image.filename))

    # Return the list of results
    return response
