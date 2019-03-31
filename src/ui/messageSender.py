import base64
import mimetypes
import os
import json

from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from apiclient import errors

def CreateMessage(sender, to, subject, message_text):
    # base64_content = base64.urlsafe_b64encode(message.as_bytes()).decode()
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    bytes_message = message.as_bytes()
    base64_obj = base64.urlsafe_b64encode(bytes_message)
    base64_str = base64_obj.decode()

    return {'raw': base64_str }

def sendMessage(service, user_id, message):
    try:
        msg = service.users().messages().send(userId=user_id, body=message).execute()

        return msg
    except errors.HttpError as error:
        print('An error occurred: %s' % error)

def CreateMessageWithAttachment(sender, to, subject, message_text, file_dir,
                                filename):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    msg = MIMEText(message_text)
    message.attach(msg)

    path = os.path.join(file_dir, filename)
    content_type, encoding = mimetypes.guess_type(path)

    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)
    if main_type == 'text':
        fp = open(path, 'rb')
        msg = MIMEText(fp.read(), _subtype=sub_type, _charset='utf-8')
        fp.close()
    elif main_type == 'image':
        fp = open(path, 'rb')
        msg = MIMEImage(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'audio':
        fp = open(path, 'rb')
        msg = MIMEAudio(fp.read(), _subtype=sub_type)
        fp.close()
    else:
        fp = open(path, 'rb')
        msg = MIMEBase(main_type, sub_type)
        msg.set_payload(fp.read())
        fp.close()

    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)
    base64_content = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': base64_content }
