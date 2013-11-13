keysend
=======
I had to bulk send software activation keys and needed a quick solution. keysend.py is a small python3 script that lets you send individualized content to a list of email addresses.

Basic use
---------
	python3 keysend.py

before running the script, edit the following files:
* addresses.txt - should contain the addresses of all the recipients. Tab separated name and email address. One recipient per line.
* keys.txt - should contain all the keys you want to distribute. One key per line.
* template.txt - This is a template for your email. The word [KEY] will be replaced with the key, [NAME] with the name.
* keysend.py - Use command line arguments to set the parameters

Example
-------
	python3 keysend.py -u username -p password -e smtp.server.com -f me@mydomain.com -s "Your personal key"

type this to get a list of all parameters:
	python3 keysend.py --help

This script can be easily adjusted for more complex tasks (e.g. more personalized content). It can also be used to bulk send unwanted advertising materials. Don't do this. Nobody likes spam. Also, check the rules of your SMTP server. Some providers will lock your account if you exceed your daily limits.
