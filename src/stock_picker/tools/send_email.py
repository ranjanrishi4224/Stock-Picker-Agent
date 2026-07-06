import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(subject: str, message: str) -> str:
    """
    Sends an email with the generated investment report attached.

    Args:
        subject: Email subject.
        message: Email body.

    Returns:
        Status message indicating success or failure.
    """

    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")

    sender = os.getenv("SMTP_FROM")
    recipient = os.getenv("SMTP_TO")

    if not smtp_host:
        return "SMTP_HOST is missing."

    if not smtp_username:
        return "SMTP_USERNAME is missing."

    if not smtp_password:
        return "SMTP_PASSWORD is missing."

    if not sender:
        return "SMTP_FROM is missing."

    if not recipient:
        return "SMTP_TO is missing."

    msg = MIMEMultipart()

    msg["From"] = f"Stock Picker AI <{sender}>"
    msg["To"] = recipient
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "html"))

    report_path = "output/report.pdf"

    if os.path.exists(report_path):
        try:
            with open(report_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

            encoders.encode_base64(part)

            part.add_header(
                "Content-Disposition",
                f'attachment; filename="{os.path.basename(report_path)}"',
            )

            msg.attach(part)

        except Exception as e:
            return f"Failed to attach report: {e}"

    else:
        print("Warning: output/decision.md was not found. Sending email without attachment.")

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()

            server.login(
                smtp_username,
                smtp_password,
            )

            server.send_message(msg)

        if os.path.exists(report_path):
            return "Email sent successfully with decision.md attached."

        return "Email sent successfully (no attachment found)."

    except smtplib.SMTPAuthenticationError:
        return (
            "SMTP authentication failed. "
            "Check your Gmail App Password and SMTP credentials."
        )

    except smtplib.SMTPException as e:
        return f"SMTP error: {e}"

    except Exception as e:
        return f"Unexpected error while sending email: {e}"