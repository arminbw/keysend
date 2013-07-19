keysend
=======
keysend.py is a small python3 script that lets you send unique promotion codes/activation keys to a list of email addresses

Basic use
---------
python3 keysend.py

before running the script, edit the following files:
* addresses.txt - should contain the addresses of all the recipients (line seperated)
* keys.txt - should contain all the keys you want to distribute (line seperated)
* template.txt - This is a template for your email. The word PERSONALKEY will be replaced by the script.
* keysend.py - edit the SMTP configuration and the subject line of your email

This script can be easily adjusted for more complex tasks (e.g. more personalized content). It can also be used to bulk send unwanted advertising materials. Don't do this. Nobody likes spam. Also, check the rules of your SMTP server. Some providers will lock your account if you exceed your daily limits.

