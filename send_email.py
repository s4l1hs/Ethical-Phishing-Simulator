import smtplib,ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

sender_email = "[CHANGE_ME]"
receiver_email = "[CHANGE_ME]"

message = MIMEMultipart()
message['Subject'] = "[CHANGE_ME]"
message['From'] = sender_email
message['To'] = receiver_email

text = """\
Message body goes here.
"""
part1 = MIMEText(text, 'plain')
message.attach(part1)

filePath = "[CHANGE_ME]"
part2 = MIMEBase('application', 'octet-stream')
part2.set_payload(open(filePath, 'rb').read())
encoders.encode_base64(part2)

part2.add_header('Content-Disposition', f'attachment; filename="{filePath}"')

message.attach(part2)

# Create secure connection with server and send email
context = ssl.create_default_context()
server = smtplib.SMTP("mail.securelawfirm.com", 587)
server.starttls()
server.ehlo_or_helo_if_needed()
server.sendmail(sender_email, receiver_email, message.as_string())
