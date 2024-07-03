# pylint: disable=bad-mcs-method-argument,too-few-public-methods

"""
Module that defines the model registry for Yolo Object Detection.
"""

from ultralytics import YOLO
from src.model_registry.base_model_registry import BaseModelRegistry


class YoloObjectDetectionModelRegistry(BaseModelRegistry):
    """
    Model registry for Yolo Object Detection Models.
    """

    def __init__(self, revision="8", version="n"):
        super().__init__()
        self.version = version
        self.revision = revision

    def load_model(self):
        """
        Load the YOLO Object Detection model.

        Returns:
            YOLO: The loaded YOLO model.
        """
        # Construct the model name by appending the version
        model_name = "yolov" + self.revision + self.version + ".pt"

        # Load the YOLO model using the specified model name
        model = YOLO(model_name)

        # Return the loaded model
        return model
