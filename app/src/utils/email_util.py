from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from typing import List

import os
from dotenv import load_dotenv

from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

conf = ConnectionConfig(
    MAIL_USERNAME = os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD"),
    MAIL_FROM = os.getenv("MAIL_FROM"),
    MAIL_PORT = os.getenv("MAIL_PORT"),
    MAIL_SERVER = os.getenv("MAIL_SERVER"),
    MAIL_TLS = os.getenv("MAIL_TLS"),
    MAIL_SSL = os.getenv("MAIL_SSL"),
    USE_CREDENTIALS = os.getenv("USE_CREDENTIALS"),
    VALIDATE_CERTS = os.getenv("VALIDATE_CERTS")
)


async def send_email(subject: str, recepient: List, message: str):
    """ Function takes information for sending email (subject, list of recepients and text of message)
    and sends it with fastapi_mail """
    message = MessageSchema(
        subject=subject,
        recipients=recepient, # email.dict().get("email"),  # List of recipients, as many as you can pass 
        body=message,
        subtype="html"
        )
    fm = FastMail(conf)
    await fm.send_message(message)
