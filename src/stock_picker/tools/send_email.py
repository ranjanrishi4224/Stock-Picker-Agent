from crewai.tools import tool
import os
import smtplib
from email.mime.text import MIMEText


@tool("Send Email")
def send_email(subject: str, message: str) -> str:
    """
    Sends an email to the configured recipient.
    """

    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")

    sender = os.getenv("SMTP_FROM")
    recipient = os.getenv("SMTP_TO")

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender, recipient, msg.as_string())

        return "Email sent successfully."

    except Exception as e:
        return f"Failed to send email: {e}"