import ConfigParser
import os
from django.core import signing

folder = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(folder, 'config.ini'))
links_file_path = os.path.abspath(os.path.join(folder, 'links.ini'))

def get_email_info():
    return read_config(file_path, 'email')

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

def read_config(file_path, section):
    config = ConfigParser.RawConfigParser()
    config.read(file_path)
    if config.has_section(section):
        return dict( i for i in config.items(section) )

    return None

def read_links():
    return read_config(links_file_path, 'links')

def write_links(links):
    config = ConfigParser.RawConfigParser()
    config_file = open(links_file_path, 'wb')
    config.add_section('links')
    for k, v in links.items():
        config.set('links', k, v)

    config.write(config_file)
    config_file.close()