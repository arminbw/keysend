#!/usr/bin/env python3

import sys, argparse, smtplib
from email.mime.text import MIMEText

smtp_user = 'johndoe1972@example.com'      # smtp user name for authentification
smtp_password = '12345'                    # smtp password for authentification
smtp_server = 'smtp.example.com'           # smtp server address
from_address = 'myOwnAddress@example.com'  # email address of the sender (that's you!)
subject = 'Your personal key'              # subject of the email
addresses_filename = 'addresses.txt'       # file with one email address per line
keys_filename = 'keys.txt'                 # file with one key per line
template_filename = 'template.txt'         # template file for the email

def send_email(from_address, to_address, text, subject):
    message = MIMEText(text)
    message['From'] = from_address
    message['To'] = to_address
    message['Subject'] = subject
    try:
        server.sendmail(from_address, to_address, message.as_string())
        print('mail sent successfully.\n')
    except:
        print('failed to send mail.\n')
        server.close()
        raise

def get_file_content(filename):
    with open(filename, 'r') as fp:
        content = fp.read()
    return content

addresses = get_file_content(addresses_filename).splitlines()
keys = get_file_content(keys_filename).splitlines()
if len(addresses) > len(keys):
    print('not enough keys provided (%i addresses, only %i keys)' % (len(addresses), len(keys)))
    sys.exit(1)
template = get_file_content(template_filename)

try:
    server = smtplib.SMTP(smtp_server, 587)
    server.ehlo()
    server.starttls()
    server.login(smtp_user, smtp_password)
except smtplib.SMTPAuthenticationError:
    print('failed to connect to smtp server. Username or password wrong.')
    sys.exit(1)
except:
    print('failed to connect to smtp server.')
    raise

keyNumber = 0
for address in addresses:
    text = template.replace("PERSONALKEY", keys[keyNumber])    
    print("email no.%i    address: %s    key: %s" % (keyNumber+1, address, keys[keyNumber]))
    send_email(from_address, address, text, subject)
    keyNumber += 1
server.close()
