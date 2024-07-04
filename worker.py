from celery import Celery

from configs.config import get_settings


worker = Celery(
     "worker",
     broker=get_settings().CELERY_BROKER_URL,
     backend=get_settings().CELERY_RESULT_BACKEND,
     include=["src.services.notification.notification_service"],
)
