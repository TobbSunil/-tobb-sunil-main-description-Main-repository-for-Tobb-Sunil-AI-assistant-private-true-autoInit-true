#!/usr/bin/env python3
"""Fetch unread Gmail messages via IMAP with App Password."""
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

def fetch_unread_emails(limit=10, as_json=False):
    """Fetch unread emails.

    Returns a list of dictionaries with keys: from, subject, date, body_preview.
    If ``as_json`` is True, returns a JSON string instead of printing.
    """
    addr, pwd = load_credentials()
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(addr, pwd)
    mail.select('inbox')

    typ, data = mail.search(None, 'UNSEEN')
    if typ != 'OK':
        mail.logout()
        raise RuntimeError('Search failed')

    ids = data[0].split()
    results = []
    for num in ids[:limit]:
        typ, msg_data = mail.fetch(num, '(RFC822)')
        if typ != 'OK':
            continue
        msg = email.message_from_bytes(msg_data[0][1])
        subject = decode_str(msg.get('Subject', ''))
        sender = decode_str(msg.get('From', ''))
        date = msg.get('Date', '')
        body = get_body(msg)
        preview = body[:500] + ('...' if len(body) > 500 else '')
        # Mark as SEEN
        mail.store(num, '+FLAGS', '\\Seen')
        results.append({
            'from': sender,
            'subject': subject,
            'date': date,
            'body_preview': preview,
        })
    mail.logout()
    if as_json:
        import json
        return json.dumps(results)
    return results


def main():
    import sys, json
    # If called with '--json' flag, output JSON
    if '--json' in sys.argv:
        limit = 10
        if len(sys.argv) > 2 and sys.argv[2].isdigit():
            limit = int(sys.argv[2])
        print(fetch_unread_emails(limit=limit, as_json=True))
        return
    # Default human-readable output
    emails = fetch_unread_emails()
    print(f'Unread messages: {len(emails)}')
    for email_data in emails:
        print('\n--- Message ---')
        print(f"From: {email_data['from']}")
        print(f"Date: {email_data['date']}")
        print(f"Subject: {email_data['subject']}")
        print(f"Body:\n{email_data['body_preview']}")

if __name__ == '__main__':
    main()

