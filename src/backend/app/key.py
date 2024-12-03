# from flask import current_app
#
# print("Secret Key:", current_app.app.config['SECRET_KEY'])


# import smtplib
#
# sender = 'noreply@walletwizard.com'
# recipient = 'test@example.com'
# subject = "Test Email"
# body = "This is a test email."
#
# message = f"Subject: {subject}\n\n{body}"
#
# try:
#     with smtplib.SMTP('localhost', 1025) as smtp:
#         smtp.sendmail(sender, recipient, message)
#         print("Email sent successfully!")
# except Exception as e:
#     print(f"Failed to send email: {e}")

import smtplib
from email.mime.text import MIMEText

sender = 'noreply@walletwizard.com'
recipient = 'test@example.com'
subject = "Test Email"
body = "This is a test email."

message = MIMEText(body)
message['Subject'] = subject
message['From'] = sender
message['To'] = recipient

try:
    with smtplib.SMTP('localhost', 1025) as smtp:
        smtp.sendmail(sender, recipient, message.as_string())
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")