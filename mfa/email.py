import os
from smtplib import SMTP_SSL

from email.message import EmailMessage


def _get_email_string(user_email, text):
    # sender_email = os.getenv("MFA_EMAIL_ADDRESS")
    subject = "Verification code for testing..."
    message = EmailMessage()
    message["To"] = user_email
    message["From"] = os.getenv("MFA_EMAIL_ADDRESS")
    message["Subject"] = subject
    message.set_content(text)
    return message.as_string()


def send_mfa_email(user_email, confirmation_code):

    sender_email = os.getenv("MFA_EMAIL_ADDRESS")
    confirmation_code = 8256

    sender_password = os.getenv("MFA_EMAIL_PASSWORD")
    user_email = os.getenv("MFA_EMAIL_TEST_RECIPIENT")  # TODO: add for testing
    smtp = os.getenv("MFA_EMAIL_SMTP")

    text = f"Your 2fa code is {confirmation_code}"

    try:
        message = _get_email_string(user_email, text)

        ###################################################################
        # TODO: KEEP RETURN STATEMENT DURING DEV TO AVOID ACCIDENTAL SEND #
        ###################################################################
        return True
        # smtp_server = SMTP_SSL(smtp, 465)
        smtp_server = SMTP_SSL(smtp)
        smtp_server.login(sender_email, sender_password)
        smtp_server.sendmail(sender_email, user_email, message)
    except Exception as e:
        print("Error sending email:", e)
    finally:
        smtp_server.quit()
