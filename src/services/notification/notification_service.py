from jinja2 import Template
from worker import worker
from src.services.notification.email_notifier import EmailNotifier
from src.utils.notification.constants import EMAIL_TEMPLATE_MAPPING
from src.utils.vehicle_detection.types import NotificationTo


@worker.task(name="notify")
def notify(data: dict, notify_to: str) -> None:
     if notify_to == NotificationTo.EMAIL.value:
          notify_using_email(data)
     else:
          raise NotImplementedError("Notification service not implemented")


def notify_using_email(data: dict) -> None:
     email_service = EmailNotifier()
     try:
          if email_service.validate_notification(data):
               template_path = EMAIL_TEMPLATE_MAPPING[data["template"]]
               with open(template_path, "r") as f:
                    data["template"] = f.read()
               jinja_template = Template(source=data["template"])
               email_data = jinja_template.render(data["message"])
               data["message"] = email_data
               email_service.send_notification(**data)
     except Exception as e:
          raise e
     finally:
          email_service.close_connection()
