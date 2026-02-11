#!/usr/bin/env python3
"""Run the daily Gmail fetch and reply tasks.
It calls fetch_mail.py (to log unread count) and then
respond_to_kallstrom.py (to reply to any unseen mail from
linux.kallstrom@gmail.com). All output is appended to a log file.
"""
import subprocess
import datetime
import os

log_file = '/home/tobsun/.openclaw/workspace/gmail_imap/mail_tasks.log'

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout + result.stderr

now = datetime.datetime.now().isoformat()
header = f"\n=== {now} ===\n"

# Run fetch_mail
fetch_output = run_cmd('/home/tobsun/.openclaw/workspace/gmail_imap/fetch_mail.py')
# Run respond_to_kallstrom (may succeed or fail)
respond_output = run_cmd('/home/tobsun/.openclaw/workspace/gmail_imap/respond_to_kallstrom.py')

with open(log_file, 'a') as f:
    f.write(header)
    f.write('--- fetch_mail output ---\n')
    f.write(fetch_output)
    f.write('\n--- respond_to_kallstrom output ---\n')
    f.write(respond_output)
    f.write('\n')

print('Mail tasks completed; output logged to', log_file)
