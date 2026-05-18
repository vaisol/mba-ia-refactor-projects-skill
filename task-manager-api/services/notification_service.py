import smtplib
from config import Config

class NotificationService:
    def __init__(self):
        self.email_user = Config.EMAIL_USER
        self.email_password = Config.EMAIL_PASS

    def send_email(self, to, subject, body):
        # Implementation using Config...
        print(f"Simulando envio de email para {to} usando {self.email_user}")
        return True
