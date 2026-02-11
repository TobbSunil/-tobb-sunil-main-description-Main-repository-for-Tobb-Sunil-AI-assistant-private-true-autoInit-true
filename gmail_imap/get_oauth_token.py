#!/usr/bin/env python3
"""Utility to obtain a Google OAuth refresh token for Gmail IMAP access.

Prerequisites:
- Install required libs: google-auth, google-auth-oauthlib
- Have a `client_secret.json` file in `~/workspace/credentials/`

The script runs the OAuth flow in a local browser, then saves the refresh token
to `~/workspace/credentials/gmail_oauth_refresh.txt`.
"""
import os
import json
from pathlib import Path

# Paths
CLIENT_SECRET_PATH = '/home/tobsun/.openclaw/workspace/credentials/client_secret.json'
REFRESH_TOKEN_PATH = '/home/tobsun/.openclaw/workspace/credentials/gmail_oauth_refresh.txt'

# Scopes needed for full Gmail IMAP access
SCOPES = ['https://mail.google.com/']

def main():
    # Verify client secret exists
    if not os.path.exists(CLIENT_SECRET_PATH):
        raise FileNotFoundError(f"Client secret file not found: {CLIENT_SECRET_PATH}")

    # Import after confirming file existence (so we can give a clear error if missing deps)
    from google_auth_oauthlib.flow import InstalledAppFlow

    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_PATH, SCOPES)
    # Use console flow (no local web server) – it will print a URL you can copy
    creds = flow.run_console()

    # Save the refresh token for later use
    Path(REFRESH_TOKEN_PATH).write_text(creds.refresh_token or '')
    print('Refresh token saved to', REFRESH_TOKEN_PATH)

if __name__ == '__main__':
    main()
