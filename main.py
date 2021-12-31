import imaplib
import pprint
import os
import email

from dotenv import load_dotenv

# get host and credentials
load_dotenv()

imap_host = os.getenv("IMAP_HOST")
imap_user = os.getenv("IMAP_USER")
imap_pass = os.getenv("IMAP_PASS")

# Establish SSL Connection to host
imap = imaplib.IMAP4_SSL(imap_host, port=993)

imap.login(imap_user, imap_pass)
imap.select('Inbox')

tmp, data = imap.search(None, 'ALL')
for num in data[0].split():
	email_data = {}
	_, data = imap.fetch(num, '(RFC822)')
	_, b = data[0]
	email_message = email.message_from_bytes(b)
 
	for header in ['subject', 'to', 'from', 'date']:
		print("{}: {}".format(header, email_message[header]))
		email_data[header] = email_message[header]
 
	for part in email_message.walk():
		if part.get_content_type() == "text/plain":
			body = part.get_payload(decode=True)
			email_data['body'] = body.decode()
 
	break
imap.close()