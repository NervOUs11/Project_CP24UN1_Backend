from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel, EmailStr
import smtplib
from email.message import EmailMessage
import logging
import os
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()
password = os.getenv("EMAIL_PASSWORD")


class EmailSchema(BaseModel):
    primary_recipient: EmailStr
    alternate_recipient: EmailStr
    subject: str
    body: str


# Configure logging to help capture errors
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Function to send email
def send_email(recipient: str, subject: str, body: str):
    EMAIL_ADDRESS = "noreply.kmuttrackform@gmail.com"
    EMAIL_PASSWORD = password

    try:
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = recipient
        msg.set_content(body)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        logger.info(f"Email successfully sent to {recipient}")
    except Exception as e:
        logger.error(f"Error sending email to {recipient}: {str(e)}")
        raise e


@app.post("/send-email")
async def email_notification(email: EmailSchema):
    try:
        # Attempt to send email to the primary recipient
        send_email(email.primary_recipient, email.subject, email.body)
        # logger.info(f"Send email to primary recipient: {email.primary_recipient}")
        # return {"message": f"Email is being sent to {email.primary_recipient}"}
    # except Exception as primary_error:
    #     logger.warning(f"Failed to send email to primary recipient: {email.primary_recipient}. Error: {str(primary_error)}")
    #     try:
    #         # Attempt to send email to the alternate recipient
        send_email(email.alternate_recipient, email.subject, email.body)
        # logger.info(f"Send email to alternate recipient: {email.alternate_recipient}")
        # return {"message": f"Email is being sent to alternate recipient {email.alternate_recipient}"}
    except Exception as alternate_error:
        logger.error(f"Failed to send email to both primary and alternate recipients. Primary error: {str(primary_error)}, Alternate error: {str(alternate_error)}")
        raise HTTPException(status_code=500, detail=f"Failed to send email to both recipients. Primary error: {str(primary_error)}, Alternate error: {str(alternate_error)}")