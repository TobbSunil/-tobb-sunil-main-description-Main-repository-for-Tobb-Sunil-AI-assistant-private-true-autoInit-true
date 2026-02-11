#!/usr/bin/env python3
"""Automatically reply to any unread email from linux.kallstrom@gmail.com.
The script:
  1. Calls fetch_mail.py with --json to get unread messages and mark them as SEEN.
  2. Filters messages from the target address.
  3. Sends a canned reply using send_mail.py.
"""
import subprocess
import json
import shlex
import sys

TARGET = "linux.kallstrom@gmail.com"
REPLY_SUBJECT_PREFIX = "Re: "
REPLY_BODY = """Hello Linus,

I’ve received your test email and can read it fine. Let me know if there’s anything specific you’d like assistance with.

Best regards,
Tobb Sunil ✨
"""

def main():
    # 1. Get unread emails in JSON format
    try:
        fetch_cmd = [
            sys.executable,
            "/home/tobsun/.openclaw/workspace/gmail_imap/fetch_mail.py",
            "--json",
        ]
        result = subprocess.check_output(fetch_cmd, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error fetching mail: {e}")
        sys.exit(1)

    try:
        emails = json.loads(result)
    except json.JSONDecodeError:
        print("Failed to parse JSON from fetch_mail")
        sys.exit(1)

    replied = 0
    for email in emails:
        if email.get("from", "").lower().endswith(TARGET.lower()):
            # Build subject line
            original_subject = email.get("subject", "No Subject")
            subject = REPLY_SUBJECT_PREFIX + original_subject
            # Use the send_mail script
            send_cmd = [
                sys.executable,
                "/home/tobsun/.openclaw/workspace/gmail_imap/send_mail.py",
                TARGET,
                subject,
                REPLY_BODY,
            ]
            try:
                subprocess.check_call(send_cmd)
                replied += 1
            except subprocess.CalledProcessError as e:
                print(f"Failed to send reply for {original_subject}: {e}")
    if replied == 0:
        print("No unread emails from the target address.")
    else:
        print(f"Sent {replied} reply(s) to {TARGET}.")

if __name__ == "__main__":
    main()
