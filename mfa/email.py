import os
from smtplib import SMTP_SSL

from email.message import EmailMessage

# user gives username

# secret code is generated
# secret code is placed in redis cache with userID as key? TTL of 10 mins?

# email is sent to associated user email with secret code

# USE A SECRET ID IN PLACE OF THE USERNAME FOR THE SECOND REQUEST?
#   IS THERE A GOOD WAY TO CONVEY THIS?

# 2fa endpoint awaits entry of code

# if code entered via 2fa endpoint, return access and refresh token.
# class


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
        # message = EmailMessage()
        # message["To"] = user_email
        # message["From"] = sender_email
        # message["Subject"] = "Verification code for testing..."
        # message.set_content(text)
        message = _get_email_string(user_email, text)

        print(message)
        print(message)
        return True
        smtp_server = SMTP_SSL(smtp, 465)
        smtp_server.login(sender_email, sender_password)
        smtp_server.sendmail(sender_email, user_email, message)
    except Exception as e:
        print("Error sending email:", e)
    finally:
        smtp_server.quit()

    # return True
    # s = smtplib.SMTP_SSL(os.getenv("MFA_EMAIL_SMTP"))
    # with SMTP_SSL(smtp_server, 465) as smtp_server:
        # smtp_server.login(sender_email, sender_password)
        # smtp_server.sendmail(sender_email, user_email, message.as_string())
        # print("Step 3")
        # smtp_server.quit()
        # print("Step 4")

    # s.send_message(message)

    # s.quit()
    # print("Step 5")
