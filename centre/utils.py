import ConfigParser
import os
from django.core import signing

folder = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(folder, 'config.ini'))

def get_email_info():
    config = ConfigParser.RawConfigParser()
    config.read(file_path)
    return dict( i for i in config.items('email') )

def set_email_info(email):
    update_pwd = need_update(email['password'])

    config = ConfigParser.RawConfigParser()
    config_file = open(file_path, 'wb')
    config.add_section('email')
    for k, v in email.items():
        if k == 'password' and update_pwd:
            v = ecrypt(v)
        config.set('email', k, v)

    config.write(config_file)
    config_file.close()

def need_update(pwd):
    return get_email_info()['password'].strip() != pwd.strip()

def decrypt(value):
    return signing.loads(value)

def ecrypt(value):
    return signing.dumps(value)