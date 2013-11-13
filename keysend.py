#!/usr/bin/env python3

import sys, argparse, smtplib, time
from email.mime.text import MIMEText

parser = argparse.ArgumentParser(description='bulk send software keys')
parser.add_argument('--smtp_user', '-u', help='smtp username', required=True)
parser.add_argument('--smtp_password', '-p', help='smpt password', required=True)
parser.add_argument('--smtp_server', '-e', help='smpt server address', required=True)
parser.add_argument('--from_address', '-f', help='email sender address', required=True)
parser.add_argument('--subject', '-s', help='email subject', required=True)
parser.add_argument('--addresses_filename', '-a', type=argparse.FileType('r'), help='file containing lines with <name> TAB <email address>', default="addresses.txt")
parser.add_argument('--keys_filename', '-k', type=argparse.FileType('r'), help='file containing keys, one key per line', default="keys.txt")
parser.add_argument('--template_filename', '-t', help='file containing email body template. [NAME] is replaced with the name, [KEY] is replaced with key', default="template.txt")
parser.add_argument('--bcc_address', '-b', nargs='?', help='bcc address')
parser.add_argument('--dryrun', '-d', help='dry run. Do not send anything.', action="store_true")
parser.add_argument('--verbose', '-v', help='verbose mode', action="store_true")

args = parser.parse_args()

if args.verbose:
	print vars(args)

def send_email(from_address, to_address, text, subject):
	message = MIMEText(text)
	message['From'] = from_address
	message['To'] = to_address
	message['Subject'] = subject
	if args.bcc_address is not None:
		message['Bcc'] = args.bcc_address
	try:
		if args.verbose:
			print message.as_string()
		if not args.dryrun:
			server.sendmail(from_address, to_address, message.as_string())
		if args.verbose:
			print('mail sent successfully.')
	except:
		print('failed to send mail.\naborting.\n')
		server.close()
		raise

def get_file_content(filename):
	with open(filename, 'r') as fp:
		content = fp.read()
	return content

addresses = args.addresses_filename.read().splitlines()
keys = args.keys_filename.read().splitlines()
if len(addresses) > len(keys):
	print('not enough keys provided (%i addresses, only %i keys)' % (len(addresses), len(keys)))
	sys.exit(1)
template = get_file_content(args.template_filename)

try:
	server = smtplib.SMTP(args.smtp_server, 587)
	server.ehlo()
	server.starttls()
	server.login(args.smtp_user, args.smtp_password)
except smtplib.SMTPAuthenticationError:
	print('failed to connect to smtp server. Username or password wrong.')
	sys.exit(1)
except:
	print('failed to connect to smtp server.')
	raise

keyNumber = 0
for line in addresses:
	name = line.split('\t')[0]
	# name = name.split()[0] # use the first name only
	address = line.split('\t')[1]
	text = template.replace("[KEY]", keys[keyNumber])
	text = text.replace("[NAME]", name)
	print("email no.%i\tTo: %s <%s>\tKey: %s" % (keyNumber+1, name, address, keys[keyNumber]))
	send_email(args.from_address, address, text, args.subject)
	time.sleep(0.5)
	keyNumber += 1
	
server.close()
