"""
Common functions and utilities for vehicle detection
"""

import io
from fastapi import UploadFile
import numpy as np
from ultralytics.engine.results import Results
from PIL import Image

from src.utils.utils import run_in_thread


def get_results_from_yolo(result: Results, filename: str, classes: list) -> dict:
    """
    This function takes in a YOLO result and a filename, and returns a dictionary
    containing the filename and a list of predictions. Each prediction is a dictionary
    with keys 'class', 'score', and 'box'.

    Args:
        result (Results): The YOLO result.
        filename (str): The name of the file the result corresponds to.

    Returns:
        dict: A dictionary with keys 'filename' and 'predictions'.
    """
    # Get the boxes from the result
    boxes = result.boxes

    # Initialize an empty list to store predictions
    predictions = []

    # Iterate over the boxes, and convert them to a format that can be used to make predictions
    for cls, conf, box in zip(
        boxes.cls.cpu().tolist(), boxes.conf.cpu().tolist(), boxes.xyxy.cpu().tolist()
    ):
        # Make a prediction dictionary
        prediction = {
            "class": classes[cls],  # The class of the object
            "score": conf,  # The confidence score of the object
            "box": box,  # The bounding box of the object
        }

        # Add the prediction to the list of predictions
        predictions.append(prediction)

    # Return a dictionary with the filename and the list of predictions
    return {"filename": filename, "predictions": predictions}


async def convert_files_to_numpy_arrays(files: list[UploadFile]) -> dict:
    """
    This function takes in a list of UploadFile objects and converts them to a dictionary
    where the keys are filenames and the values are corresponding numpy arrays.

    Args:
        files (list[UploadFile]): A list of UploadFile objects.

    Returns:
        dict: A dictionary where the keys are filenames and the values are numpy arrays.
    """
    image_data = {}  # Initialize an empty dictionary to store the image data

    for image in files:  # Iterate over the list of UploadFile objects
        if not image:  # If the image is None, skip it
            continue

        filename = image.filename  # Get the filename of the image

        try:  # Try to convert the image to a numpy array
            img = await image.read()  # Read the image data
            img = await run_in_thread(
                io.BytesIO, img
            )  # Convert the data to a BytesIO object
            img = await run_in_thread(Image.open, img)  # Open the image using PIL
            np_img: np.ndarray = await run_in_thread(
                np.array, img
            )  # Convert the image to a numpy array

            image_data[filename] = np_img  # Add the image data to the dictionary

        except (
            Exception
        ) as e:  # If an exception occurs, raise a ValueError with the filename
            raise ValueError(f"Failed to process image {image.filename}") from e

    return image_data  # Return the dictionary containing the image data
