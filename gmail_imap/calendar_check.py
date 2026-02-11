#!/usr/bin/env python3
"""Fetch today's and tomorrow's Google Calendar events.
Uses the public iCal export URL (works without OAuth).
Falls back gracefully if calendar is private or unavailable.
"""
import json
import sys
import urllib.request
from datetime import datetime, timedelta, timezone

CRED_PATH = '/home/tobsun/.openclaw/workspace/credentials/gmail_credentials.txt'

def load_email():
    with open(CRED_PATH, 'r') as f:
        for line in f:
            if line.startswith('email:'):
                return line.split('email:')[1].strip()
    return None

def parse_ical_events(ical_text, start_dt, end_dt):
    """Minimal iCal parser — extracts VEVENT blocks with SUMMARY, DTSTART, DTEND, LOCATION."""
    events = []
    in_event = False
    current = {}
    for line in ical_text.splitlines():
        line = line.strip()
        if line == 'BEGIN:VEVENT':
            in_event = True
            current = {}
        elif line == 'END:VEVENT':
            in_event = False
            events.append(current)
        elif in_event:
            if line.startswith('SUMMARY:'):
                current['summary'] = line[8:]
            elif line.startswith('DTSTART'):
                current['start'] = line.split(':')[-1]
            elif line.startswith('DTEND'):
                current['end'] = line.split(':')[-1]
            elif line.startswith('LOCATION:'):
                current['location'] = line[9:]
    
    # Filter events by date range (basic: compare date strings)
    filtered = []
    start_str = start_dt.strftime('%Y%m%d')
    end_str = end_dt.strftime('%Y%m%d')
    for ev in events:
        dt = ev.get('start', '')[:8]
        if start_str <= dt < end_str:
            filtered.append({
                'summary': ev.get('summary', 'No title'),
                'start': ev.get('start', ''),
                'end': ev.get('end', ''),
                'location': ev.get('location', None),
            })
    return filtered

def main():
    email = load_email()
    if not email:
        print(json.dumps({'today': [], 'tomorrow': [], 'error': 'No email found'}))
        return

    # Try public iCal URL (requires calendar to be shared publicly or via link)
    ical_url = f'https://calendar.google.com/calendar/ical/{email.replace("@", "%40")}/public/basic.ics'
    
    now = datetime.now(timezone.utc)
    today_start = datetime(now.year, now.month, now.day, tzinfo=timezone.utc)
    today_end = today_start + timedelta(days=1)
    tomorrow_end = today_end + timedelta(days=1)

    try:
        req = urllib.request.Request(ical_url)
        with urllib.request.urlopen(req, timeout=10) as resp:
            ical_text = resp.read().decode('utf-8', errors='ignore')
        
        today_events = parse_ical_events(ical_text, today_start, today_end)
        tomorrow_events = parse_ical_events(ical_text, today_end, tomorrow_end)
        
        print(json.dumps({'today': today_events, 'tomorrow': tomorrow_events}, indent=2))
    except Exception as e:
        # Calendar not public or other error — return empty with note
        print(json.dumps({
            'today': [],
            'tomorrow': [],
            'note': f'Calendar not accessible ({type(e).__name__}). Make the calendar public or set up OAuth2 for full access.'
        }, indent=2))

if __name__ == '__main__':
    main()
