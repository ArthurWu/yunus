from django.core.mail import EmailMessage
from os import path
from settings import PROJECT_DIR
UPLOAD_DIR = path.abspath(path.join(PROJECT_DIR, '../upload'))

def upload(file):
    filepath = UPLOAD_DIR+file.name
    attach = open(filepath, 'wb+')
    for chunk in file.chunks():
        attach.write(chunk)
    attach.close()
    return filepath
    
def send(subject, message, from_mail, to_list, attachment):    
    msg = EmailMessage(subject, message, from_mail, to_list)
    msg.attach_file(attachment)
    msg.send()
    