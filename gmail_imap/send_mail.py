#!/usr/bin/env python3
"""Send email via Gmail SMTP with App Password.
Ensures proper line breaks by using EmailMessage (which handles CRLF conversion).
"""
import smtplib
import sys
from email.message import EmailMessage

CRED_PATH = '/home/tobsun/.openclaw/workspace/credentials/gmail_credentials.txt'
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

def load_credentials():
    creds = {}
    with open(CRED_PATH, 'r') as f:
        for line in f:
            if line.startswith('email:'):
                creds['email'] = line.split('email:')[1].strip()
            elif line.startswith('password:'):
                creds['password'] = line.split('password:')[1].strip()
    return creds['email'], creds['password']

def send_email(to_addr, subject, body, reply_to_id=None, original_msg_num=None):
    addr, pwd = load_credentials()

    msg = EmailMessage()
    msg['From'] = addr
    msg['To'] = to_addr
    msg['Subject'] = subject
    if reply_to_id:
        msg['In-Reply-To'] = reply_to_id
        msg['References'] = reply_to_id
    # Decode any escaped \n sequences so the email shows line breaks
    body = body.encode('utf-8').decode('unicode_escape')
    msg.set_content(body)

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(addr, pwd)
    server.send_message(msg)
    server.quit()
    print(f'Email sent to {to_addr}')

    # Mark original email as read if provided
    if original_msg_num:
        import imaplib
        mail = imaplib.IMAP4_SSL(SMTP_SERVER, SMTP_PORT)
        mail.login(addr, pwd)
        mail.select('inbox')
        # Ensure the message number is treated as bytes string
        mail.store(original_msg_num, '+FLAGS', '\\Seen')
        mail.logout()

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Usage: send_mail.py <to> <subject> <body> [original_msg_num]')
        sys.exit(1)
    # Optional 4th argument is original message number to mark as read
    original_msg_num = sys.argv[4] if len(sys.argv) > 4 else None
    send_email(sys.argv[1], sys.argv[2], sys.argv[3], original_msg_num=original_msg_num)
