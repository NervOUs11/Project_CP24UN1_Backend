from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
import smtplib
from email.message import EmailMessage
import logging
import os
from dotenv import load_dotenv

load_dotenv()
password = os.getenv("EMAIL_PASSWORD")


class EmailSchema(BaseModel):
    email: EmailStr
    subject: str
    body: str


# Configure logging to help capture errors
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Function to send email
async def send_email(email: EmailSchema):
    EMAIL_ADDRESS = "noreply.kmuttrackform@gmail.com"
    EMAIL_PASSWORD = password

    try:
        msg = EmailMessage()
        msg['Subject'] = email.subject
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = email.email
        msg.set_content(email.body)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        logger.info(f"Email successfully sent to {email}")
    except Exception as e:
        logger.error(f"Error sending email to {email}: {str(e)}")
        raise e

# app = FastAPI()
#
#
# @app.post("/send-email")
# async def send_email_route(email: EmailSchema):
#     send_email(email)
#     return {"message": f"Email sent to {email.email}"}