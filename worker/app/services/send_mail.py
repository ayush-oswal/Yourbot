import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

async def send_mail(subject, body, to_email):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = os.getenv("SMTP_SENDER_EMAIL")
    smtp_password = os.getenv("SMTP_SENDER_PASSWORD")

    message = MIMEText(body, 'plain')
    message['Subject'] = subject
    message['From'] = smtp_username
    message['To'] = to_email

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, to_email, message.as_string())
        server.quit()
        print(f"Email sent successfully to {to_email}")
    except Exception as e:
        print(f"Error sending email: {e}")
        raise e
