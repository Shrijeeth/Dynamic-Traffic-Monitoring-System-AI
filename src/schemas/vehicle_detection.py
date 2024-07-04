from fastapi import UploadFile
from pydantic import BaseModel

from src.utils.vehicle_detection.types import NotificationTo


class VehicleDetectionInput(BaseModel):
     notify_to: NotificationTo
     notification_addresses: list[str]
