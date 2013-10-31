#!/usr/bin/env python3

import sys, argparse, smtplib, time, csv, os
from email.mime.text import MIMEText

# smtp_user = 'u026682'					# smtp user name for authentification
# smtp_password = '1802'						# smtp password for authentification
# smtp_server = 'smtp.sil.at'				# smtp server address
# from_address = 'pi@brokenrul.es'				# email address of the sender (that's you!)
# subject = 'Your Secrets of Raetikon alpha key'  # subject of the email
# addresses_filename = 'addresses.txt'			# file with one email address per line
# keys_filename = 'keys.txt'						# file with one key per line
# template_filename = 'template.txt'				# template file for the email
# bcc_address = 'brokenrules@inbox.promoterapp.com'

parser = argparse.ArgumentParser(description='Send keys in a file to eMail addresses in another file.')
parser.add_argument('--smtp_user', '-u', help='SMTP username')
parser.add_argument('--smtp_password', '-p', help='SMTP password')
parser.add_argument('--smtp_server', '-e', help='SMTP server')
parser.add_argument('--from_address', '-f', help='From address')
parser.add_argument('--subject', '-s', help='Subject')
parser.add_argument('--addresses_filename', '-a', type=argparse.FileType('r'), help='File containing lines with <name> TAB <eMail address>')
parser.add_argument('--keys_filename', '-k', type=argparse.FileType('r'), help='File containing keys. One key per line.')
parser.add_argument('--template_filename', '-t', help='File containing eMail body template. [FIRST_NAME] is replaced with first name, [NAME] with full name and [KEY] is replaced with key')
parser.add_argument('--bcc_address', '-b', nargs='?', help='Bcc address')
parser.add_argument('--dryrun', '-d', help='Dry run. Do not send anything', action="store_true")
parser.add_argument('--verbose', '-v', help='Print verbose stuff.', action="store_true")

args = parser.parse_args()

if args.verbose:
	print vars(args)

if not (args.smtp_user and args.smtp_user and args.smtp_server and args.from_address and args.subject and args.addresses_filename and args.keys_filename and args.template_filename):
	print('Missing arguments')
	sys.exit(0)

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
			print('mail sent successfully.\n')
	except:
		print('failed to send mail.\n')
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
for line in csv.reader(addresses, delimiter="\t"):
	text = template.replace("[KEY]", keys[keyNumber])

	name = line[0].split()[0]

	text = text.replace("[NAME]", name)
	print("-- %i	To: %s <%s> Key: %s --" % (keyNumber, name, line[1], keys[keyNumber]))
	send_email(args.from_address, line[1], text, args.subject)

	time.sleep(0.5)
	keyNumber += 1
	
server.close()
