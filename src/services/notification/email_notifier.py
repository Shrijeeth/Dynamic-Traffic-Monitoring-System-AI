from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
import smtplib
from email.mime.multipart import MIMEMultipart
from configs.config import get_settings
from src.services.notification.base_notifier import BaseNotifier
from src.utils.notification.types import EmailTemplate


class EmailNotifier(BaseNotifier):
     def __init__(self) -> None:
          super().__init__()
          self.server = smtplib.SMTP(
               host=get_settings().SMTP_HOST,
               port=get_settings().SMTP_PORT,
          )
          self.server.starttls()
          self.server.login(
               user=get_settings().SMTP_USERNAME,
               password=get_settings().SMTP_PASSWORD,
          )


     def validate_notification(self, data: dict):
          validation = data["subject"] is not None and type(data["subject"]) is str
          validation = validation and data["from_mail"] is not None and type(data["from_mail"]) is str
          validation = validation and data["to_mail"] is not None and type(data["to_mail"]) is list
          validation = validation and data["message"] is not None and type(data["message"]) is dict
          validation = validation and data["template"] is not None and type(data["template"]) is int
          return validation

     def send_notification(self, subject: str, from_mail: str, to_mail: list[str], message: str, attachments: list[str] | None = None, **kwargs):
          mail = MIMEMultipart()
          mail["Subject"] = subject
          mail["From"] = from_mail
          mail["To"] = ", ".join(to_mail)
          mail.attach(MIMEText(message, "html"))

          if attachments:
               for attachment in attachments:
                    with open(attachment, "rb") as file:
                         part = MIMEBase("application", "octet-stream")
                         part.set_payload(file.read())
                         encoders.encode_base64(part)
                         part.add_header(
                              "Content-Disposition",
                              f"attachment; filename= {attachment}",
                         )
                         mail.attach(part)
          self.server.sendmail(from_mail, to_mail, mail.as_string())

     def close_connection(self):
          self.server.close()
