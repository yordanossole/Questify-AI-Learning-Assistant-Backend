import smtplib
from pathlib import Path
from email.message import EmailMessage
from jinja2 import Environment, FileSystemLoader, select_autoescape
from app.core.config import SMTP_HOST, SMTP_PORT, APP_EMAIL, GMAIL_APP_PASSWORD

TEMPLATES_DIR = Path(__file__).parent / "templates"

env = Environment(
    loader=FileSystemLoader(str(TEMPLATES_DIR)),
    autoescape=select_autoescape(['html', 'xml'])
)

class Mailer:
    def send_email(self, to_email: str, subject: str, template_name: str, context: dict):
        template = env.get_template(template_name)
        html_content = template.render(**context, app_email=APP_EMAIL)

        msg = EmailMessage()
        msg.set_content("Please view this email in an HTML-capable client.")
        msg.add_alternative(html_content, subtype="html")
        msg['Subject'] = subject
        msg['From'] = APP_EMAIL
        msg['To'] = to_email

        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as smtp:
            smtp.login(APP_EMAIL, GMAIL_APP_PASSWORD)
            smtp.send_message(msg)