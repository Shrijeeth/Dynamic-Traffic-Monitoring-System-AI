# pylint: disable=bad-mcs-method-argument,too-few-public-methods

"""
Module that defines the model registry for YoloV8.
"""

from ultralytics import YOLO
from src.model_registry.base_model_registry import BaseModelRegistry


class YoloV8ModelRegistry(BaseModelRegistry):
    """
    Model registry for YoloV8.
    """

    def __init__(self, version="n"):
        super().__init__()
        self.version = version

    def load_model(self):
        """
        Load the YOLOv8 model.

        Returns:
            YOLO: The loaded YOLOv8 model.
        """
        # Construct the model name by appending the version to 'yolov8'
        model_name = "yolov8" + self.version + ".pt"

        # Load the YOLOv8 model using the specified model name
        model = YOLO(model_name)

        # Return the loaded model
        return model
