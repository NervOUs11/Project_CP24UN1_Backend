from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel, EmailStr
import smtplib
from email.message import EmailMessage
import logging

app = FastAPI()

# Define the request body for sending email
class EmailSchema(BaseModel):
    recipient: EmailStr
    subject: str
    body: str

# Configure logging to help capture errors
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to send email
def send_email(recipient: str, subject: str, body: str):
    EMAIL_ADDRESS = "nitis.v@mail.kmutt.ac.th"
    EMAIL_PASSWORD = "bbft loxn qrgu rfpa"

    try:
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = recipient
        msg.set_content(body)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        logger.info(f"Email sent to {recipient}")
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        raise


# FastAPI endpoint to trigger email
@app.post("/send-email")
async def email_notification(email: EmailSchema, background_tasks: BackgroundTasks):
    try:
        background_tasks.add_task(send_email, email.recipient, email.subject, email.body)
        return {"message": "Email is being sent in the background"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")
