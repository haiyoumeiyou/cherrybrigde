import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Dict, List


class MailHandler(object):
    def __init__(self, mail_host:str, mail_port:int, sender_email:str=None, sender_pass:str=None):
        self.mail_host = mail_host
        self.mail_port = mail_port
        self.sender_email = sender_email
        self.sender_pass = sender_pass

    def validate_data(self, required_fields:tuple, data:Dict):
        required_fields = required_fields
        missing_fields = []
        for field in required_fields:
            if not field in data:
                missing_fields.append(field)
        return missing_fields

    def prep_msg_body(self, data:Dict):
        msg = MIMEMultipart("alternative")
        msg["Subject"] = data.get('subject')
        msg["From"] = data.get('sender')
        msg["To"] = ", ".join(data.get('recipients'))
        msg_body = MIMEText(data.get('content'), "plain")
        msg.attach(msg_body)
        return msg

    def prep_msg_attchment(self, msg:MIMEMultipart, data:Dict):
        msg = msg
        attachments = data.get('attachments')
        for attachment in attachments:
            with open(attachment, "rb") as attached:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attached.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename={attachment[9:]}",
                )
                msg.attach(part)
        return msg

    def make_plain_msg(self, data:Dict):
        required_fields = ('subject', 'sender', 'recipients', 'content')
        data_valid_check = self.validate_data(required_fields, data)
        if len(data_valid_check)>0:
            return False, data_valid_check
        return True, self.prep_msg_body(data)


    def make_attachment_msg(self, data:Dict):
        required_fields = ('subject', 'sender', 'recipients', 'content', 'attachments')
        data_valid_check = self.validate_data(required_fields, data)
        if len(data_valid_check)>0:
            return False, data_valid_check
        msg = self.prep_msg_body(data)
        return True, self.prep_msg_attchment(msg, data)

    def send_mail(self, data:Dict, credential:Dict=None):
        if 'attachments' in data:
            ready, msg = self.make_attachment_msg(data)
        else:
            ready, msg = self.make_plain_msg(data)
        if not ready:
            return False, "not able to prepare message!"
        context = ssl.create_default_context()
        with smtplib.SMTP(self.mail_host, self.mail_port) as server:
            # server.login(sender_email, password)
            print("Sending mail...", data.get('sender'), data.get('recipients'), msg)
            server.sendmail(data.get('sender'), data.get('recipients'), msg.as_string())
            return True, "message sent."

    def send_mail_o365(self, data:Dict, credential:Dict=None):
        if 'attachments' in data:
            ready, msg = self.make_attachment_msg(data)
        else:
            ready, msg = self.make_plain_msg(data)
        if not ready:
            return False, "not able to prepare message!"
        with smtplib.SMTP(self.mail_host, self.mail_port) as server:
            server.ehlo()
            server.starttls()
            server.login(self.sender_email, self.sender_pass)
            server.sendmail(data.get('sender'), data.get('recipients'), msg.as_string())
            return True, "message sent."