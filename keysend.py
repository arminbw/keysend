#!/usr/bin/env python3

import sys, argparse, smtplib, time, csv, os
from email.mime.text import MIMEText





parser = argparse.ArgumentParser(description='Send keys in a file to eMail addresses in another file.')
parser.add_argument('--smtp_user', '-u', help='SMTP username')
parser.add_argument('--smtp_password', '-p', nargs=1, help='SMTP password')
parser.add_argument('--smtp_server', '-e', nargs=1, help='SMTP server')
parser.add_argument('--from_address', '-f', nargs=1, help='From address')
parser.add_argument('--subject', '-s', nargs=1, help='Subject')
parser.add_argument('--addresses_filename', '-a', nargs=1, type=argparse.FileType('r'), help='File containing lines with <name> TAB <eMail address>')
parser.add_argument('--keys_filename', '-k', nargs=1, type=argparse.FileType('r'), help='File containing keys. One key per line.')
parser.add_argument('--template_filename', '-t', nargs=1, help='File containing eMail body template. [FIRST_NAME] is replaced with first name, [NAME] with full name and [KEY] is replaced with key')
parser.add_argument('--bcc_address', '-b', nargs='?', help='Bcc address')
parser.add_argument('--dryrun', '-d', help='Dry run. Do not send anything', action="store_true")

class Args(object):
	pass

args = parser.parse_args()
print vars(args)

dryrun = False
if args.dryrun:
	dryrun = True

bcc = False
if args.bcc_address is not None:
	bcc = True

def send_email(from_address, to_address, text, subject):
	message = MIMEText(text)
	message['From'] = args.from_address
	message['To'] = args.to_address
	message['Subject'] = args.subject
	if bcc:
		message['Bcc'] = args.bcc_address
	try:
		if dryrun:
			print message.as_string()
		else:
			# server.sendmail(from_address, to_address, message.as_string())
			print "sendmail"
		print('mail sent successfully.\n')
	except:
		print('failed to send mail.\n')
		server.close()
		raise

def get_file_content(filename):
	with open(filename, 'r') as fp:
		content = fp.read()
	return content

addresses = get_file_content(args.addresses_filename).splitlines()
keys = get_file_content(args.keys_filename).splitlines()
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
for line in csv.reader(addresses, delimiter="\t"):
	text = template.replace("[KEY]", keys[keyNumber])

	name = line[0].split()[0]

	text = text.replace("[NAME]", name)
	print("-- %i	To: %s <%s> Key: %s --" % (keyNumber, name, line[1], keys[keyNumber]))
	send_email(args.from_address, line[1], text, args.subject)

	time.sleep(0.5)
	keyNumber += 1
	
server.close()
