import smtplib
from email.mime.text import MIMEText

from fastapi_mail import MessageSchema, FastMail
from jinja2 import Environment, FileSystemLoader
from pydantic import EmailStr

from core.config import settings
from core.connection_config import conf


# Function to send password reset email / with FastMail
async def send_password_reset_email(user_id: str, email: EmailStr, token: str):
    url = f'https://yourdomain.com/reset-password/{user_id}&{token}'
    text_link = f'Restablecer contraseña'
    message = MessageSchema(
        subject='Password Reset Request',
        recipients=[email],
        body=f'Click on the link to reset your password: <a href="{url}">{text_link}</a>',
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message)


# Function to send password reset email / with smtplib
class EmailService:
    def __init__(self):
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.smtp_username = settings.SMTP_USERNAME
        self.smtp_password = settings.SMTP_PASSWORD
        self.env = Environment(loader=FileSystemLoader('templates'))

    async def create_password_reset_message(self, user_id: str, email: EmailStr, token: str) -> MIMEText:
        url = f'https://yodomain.com/reset-password/?id={user_id}&token={token}'
        text_link = f'Restablecer contraseña'
        template = self.env.get_template('password_reset_message.html')
        text_message = template.render(url=url, text_link=text_link)
        message = MIMEText(text_message, "html")
        message['Subject'] = 'Password Reset Request'
        message['To'] = email
        await self._send_email(message)

    async def create_verify_email_message(self, user_id: str, email: EmailStr, token: str) -> MIMEText:
        url = f'https://yodomain.com/verificar-email/?id={user_id}&token={token}'
        text_link = f'Confirmar correo'
        template = self.env.get_template('email_verification_message.html')
        text_message = template.render(url=url, text_link=text_link)
        message = MIMEText(text_message, "html")
        message['Subject'] = 'We will confirm your email'
        message['To'] = email
        await self._send_email(message)

    async def _send_email(self, message: MIMEText):
        mailServer = smtplib.SMTP(self.smtp_server, self.smtp_port)
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(self.smtp_username, self.smtp_password)
        mailServer.sendmail(self.smtp_username, message['To'], message.as_string())
        mailServer.close()
