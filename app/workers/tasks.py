from fastapi import BackgroundTasks

from app.services.email import EmailService

email_service = EmailService()

async def send_email(background_tasks: BackgroundTasks, recipient: str):
    subject = "Welcome to Electro Store"
    body = "Thanks for sign up in Electro Store"
    background_tasks.add_task(email_service.send_email, recipient, subject, body)