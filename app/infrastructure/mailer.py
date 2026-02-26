import smtplib
from pathlib import Path
from email.message import EmailMessage
from jinja2 import Environment, FileSystemLoader, select_autoescape
from app.core.config import settings

TEMPLATES_DIR = Path(__file__).parent / "templates"

env = Environment(
    loader=FileSystemLoader(str(TEMPLATES_DIR)),
    autoescape=select_autoescape(['html', 'xml'])
)

class Mailer:
    def send_email(self, to_email: str, subject: str, template_name: str, context: dict):
        template = env.get_template(template_name)
        html_content = template.render(**context, app_email=settings.APP_EMAIL)

        msg = EmailMessage()
        msg.set_content("Please view this email in an HTML-capable client.")
        msg.add_alternative(html_content, subtype="html")
        msg['Subject'] = subject
        msg['From'] = settings.APP_EMAIL
        msg['To'] = to_email

        with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as smtp:
            smtp.login(settings.APP_EMAIL, settings.GMAIL_APP_PASSWORD)
            smtp.send_message(msg)