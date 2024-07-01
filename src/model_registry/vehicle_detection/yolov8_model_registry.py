# pylint: disable=bad-mcs-method-argument

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
        A method to load yolov8 model.
        """
        model_name = "yolov8" + self.version + ".pt"
        model = YOLO(model_name)
        return model
