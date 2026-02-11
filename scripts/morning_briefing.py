#!/usr/bin/env python3
"""Generate a morning briefing.
Steps:
1. Get email digest JSON and format a short summary.
2. Get calendar events for today.
3. Fetch Stockholm weather from wttr.in.
4. Print a nicely formatted briefing.
"""
import json
import subprocess
import sys
import datetime
import urllib.request

def get_email_summary():
    try:
        out = subprocess.check_output([
            sys.executable, '/home/tobsun/.openclaw/workspace/gmail_imap/email_digest.py'
        ])
        emails = json.loads(out)
    except Exception as e:
        return f"Error fetching emails: {e}"
    if not emails:
        return "No new unread emails."
    lines = ["Unread Emails:"]
    for i, e in enumerate(emails, 1):
        lines.append(f"{i}. From: {e['from']} | Subject: {e['subject']} | Preview: {e['preview']} ")
    return '\n'.join(lines)

def get_calendar_summary():
    try:
        out = subprocess.check_output([
            sys.executable, '/home/tobsun/.openclaw/workspace/gmail_imap/calendar_check.py'
        ])
        data = json.loads(out)
    except Exception as e:
        return f"Error fetching calendar: {e}"
    today = data.get('today', [])
    if not today:
        return "No events today."
    lines = ["Today's Calendar Events:"]
    for ev in today:
        lines.append(f"- {ev['summary']} ( {ev['start']} to {ev['end']} )")
    return '\n'.join(lines)

def get_weather():
    WMO_CODES = {0:'Clear',1:'Mainly clear',2:'Partly cloudy',3:'Overcast',
        45:'Fog',48:'Rime fog',51:'Light drizzle',53:'Drizzle',55:'Heavy drizzle',
        61:'Light rain',63:'Rain',65:'Heavy rain',71:'Light snow',73:'Snow',75:'Heavy snow',
        77:'Snow grains',80:'Light showers',81:'Showers',82:'Heavy showers',
        85:'Light snow showers',86:'Heavy snow showers',95:'Thunderstorm'}
    try:
        url = 'https://api.open-meteo.com/v1/forecast?latitude=59.33&longitude=18.07&current=temperature_2m,weathercode,windspeed_10m,apparent_temperature&timezone=Europe/Stockholm'
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = json.load(resp)
        cur = data['current']
        desc = WMO_CODES.get(cur['weathercode'], f"Code {cur['weathercode']}")
        weather = f"{desc}, Temp: {cur['temperature_2m']}°C, Feels like: {cur['apparent_temperature']}°C, Wind: {cur['windspeed_10m']} km/h"
        return weather
    except Exception as e:
        return f"Error fetching weather: {e}"

def main():
    now = datetime.datetime.now().strftime('%A, %Y-%m-%d %H:%M')
    print(f"--- Morning Briefing ({now}) ---\n")
    print(get_email_summary())
    print('\n')
    print(get_calendar_summary())
    print('\n')
    print('Stockholm Weather:')
    print(get_weather())
    print('\n')
    print('--- End of Briefing ---')

if __name__ == '__main__':
    main()
