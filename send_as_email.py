import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime

def send_as_email(email_recipient, message_text):

        current_date = datetime.datetime.today().strftime ('%m/%d/%Y')
        subject = f"Math Quiz Results ({current_date})"
        #sender_email = "" Insert email here
        #password = "" Insert password here
        receiver_email = email_recipient

        context = ssl.create_default_context()
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message_text)
            return True
        except:
            return False
