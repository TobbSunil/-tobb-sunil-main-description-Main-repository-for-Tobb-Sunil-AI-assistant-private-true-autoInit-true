#!/usr/bin/env python3
import imaplib, smtplib, email, os
import json, urllib.parse, urllib.request
from email.message import EmailMessage

# Paths & credentials
cred_path = '/home/tobsun/.openclaw/workspace/credentials/gmail_credentials.txt'

# Load credentials
email_addr = None
password = None
with open(cred_path, 'r') as f:
    for line in f:
        if line.startswith('email:'):
            email_addr = line.split('email:')[1].strip()
        elif line.startswith('password:'):
            password = line.split('password:')[1].strip()

# Ensure exact values (remove stray whitespace)
email_addr = email_addr.strip()
password = password.strip()

if not email_addr or not password:
    raise RuntimeError('Missing credentials')

IMAP_SERVER = 'imap.gmail.com'
IMAP_PORT = 993
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

# Connect to IMAP
mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)

# ----- OAuth2 login -----
# Load client secret and refresh token
CLIENT_SECRET_PATH = '/home/tobsun/.openclaw/workspace/credentials/client_secret.json'
REFRESH_TOKEN_PATH = '/home/tobsun/.openclaw/workspace/credentials/gmail_oauth_refresh.txt'

import json, urllib.parse, urllib.request

# Read the stored refresh token
with open(REFRESH_TOKEN_PATH, 'r') as f:
    refresh_token = f.read().strip()

# Load client ID/secret
with open(CLIENT_SECRET_PATH, 'r') as f:
    client_info = json.load(f)['installed']
client_id = client_info['client_id']
client_secret = client_info['client_secret']

# Exchange refresh token for an access token via HTTP POST
token_url = 'https://oauth2.googleapis.com/token'
post_data = urllib.parse.urlencode({
    'client_id': client_id,
    'client_secret': client_secret,
    'refresh_token': refresh_token,
    'grant_type': 'refresh_token'
}).encode()
req = urllib.request.Request(token_url, data=post_data, method='POST')
with urllib.request.urlopen(req) as resp:
    token_response = json.load(resp)
access_token = token_response['access_token']

# Prepare the XOAUTH2 authentication string
auth_string = f"user={email_addr}\1auth=Bearer {access_token}\1\1".encode()
mail.authenticate('XOAUTH2', lambda x: auth_string)

mail.select('inbox')

# Search for UNSEEN messages from linux.kallstrom@gmail.com
status, data = mail.search(None, '(UNSEEN FROM "linux.kallstrom@gmail.com")')
if status != 'OK':
    print('Search failed')
    mail.logout()
    exit(1)

msg_ids = data[0].split()
if not msg_ids:
    print('No unseen messages from linux.kallstrom@gmail.com')
    mail.logout()
    exit(0)

# We'll respond to the most recent one (last ID)
latest_id = msg_ids[-1]
status, msg_data = mail.fetch(latest_id, '(RFC822)')
if status != 'OK':
    print('Fetch failed')
    mail.logout()
    exit(1)

raw_email = msg_data[0][1]
orig_msg = email.message_from_bytes(raw_email)
orig_subject = orig_msg.get('Subject', '(No Subject)')
orig_from = orig_msg.get('From')
orig_msgid = orig_msg.get('Message-ID')

# Compose reply
reply = EmailMessage()
reply['Subject'] = 'Re: ' + orig_subject
reply['From'] = email_addr
reply['To'] = email_addr  # replying to self (you can change as needed)
reply['In-Reply-To'] = orig_msgid
reply['References'] = orig_msgid
reply.set_content('Hello,\n\nI have received your email and will get back to you shortly.\n\nBest regards,\nTobb')

# Send via SMTP
smtp = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
smtp.starttls()
smtp.login(email_addr, password)
smtp.send_message(reply)
smtp.quit()

print(f'Sent reply to {orig_from} (Message-ID: {orig_msgid})')

mail.logout()
