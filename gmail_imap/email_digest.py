#!/usr/bin/env python3
"""Fetch all unread emails, mark them as read, and output a JSON summary.
Each entry contains: from, subject, date, preview (first 200 chars).
"""
import json
import sys
import imaplib
import email
from email.header import decode_header

CRED_PATH = '/home/tobsun/.openclaw/workspace/credentials/gmail_credentials.txt'
IMAP_SERVER = 'imap.gmail.com'
IMAP_PORT = 993

def load_credentials():
    creds = {}
    with open(CRED_PATH, 'r') as f:
        for line in f:
            if line.startswith('email:'):
                creds['email'] = line.split('email:')[1].strip()
            elif line.startswith('password:'):
                creds['password'] = line.split('password:')[1].strip()
    return creds['email'], creds['password']

def decode_str(s):
    if s is None:
        return ''
    parts = decode_header(s)
    result = []
    for part, charset in parts:
        if isinstance(part, bytes):
            result.append(part.decode(charset or 'utf-8', errors='ignore'))
        else:
            result.append(part)
    return ''.join(result)

def get_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            ct = part.get_content_type()
            if ct == 'text/plain' and 'attachment' not in str(part.get('Content-Disposition', '')):
                payload = part.get_payload(decode=True)
                if payload:
                    charset = part.get_content_charset() or 'utf-8'
                    return payload.decode(charset, errors='ignore')
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            charset = msg.get_content_charset() or 'utf-8'
            return payload.decode(charset, errors='ignore')
    return ''

def main():
    addr, pwd = load_credentials()
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(addr, pwd)
    mail.select('inbox')
    typ, data = mail.search(None, 'UNSEEN')
    if typ != 'OK':
        mail.logout()
        print(json.dumps({'error': 'search failed'}))
        sys.exit(1)
    ids = data[0].split()
    summaries = []
    for num in ids:
        typ, msg_data = mail.fetch(num, '(RFC822)')
        if typ != 'OK':
            continue
        msg = email.message_from_bytes(msg_data[0][1])
        subject = decode_str(msg.get('Subject', ''))
        sender = decode_str(msg.get('From', ''))
        date = msg.get('Date', '')
        body = get_body(msg)
        preview = (body[:200] + ('...' if len(body) > 200 else ''))
        # Mark as SEEN
        mail.store(num, '+FLAGS', '\\Seen')
        summaries.append({
            'from': sender,
            'subject': subject,
            'date': date,
            'preview': preview,
        })
    mail.logout()
    print(json.dumps(summaries, indent=2))

if __name__ == '__main__':
    main()
