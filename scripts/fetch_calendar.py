#!/usr/bin/env python3
"""Fetch public Google Calendar .ics and write upcoming events to data/calendar_events.json

Usage:
  python3 scripts/fetch_calendar.py

Reads calendar ID from hugo.toml `params.googleCalendar.calendarId` if available, or set CALENDAR_ID env var.
Writes `data/calendar_events.json` with an array of events: {title, start_iso, end_iso, location, description, url}
Only future events (starting >= now) are included, sorted by start time. By default takes next 8 events.
"""

import os
import sys
import json
import datetime
import requests
import pathlib
import re

try:
    from dateutil import tz, parser as dateparser
except Exception:
    print("Missing dependency: python-dateutil. Install with: pip install python-dateutil")
    sys.exit(1)


DEFAULT_MAX = 8
OUT_PATH = pathlib.Path('data/calendar_events.json')

# Try to read calendar id from hugo.toml
CALENDAR_ID = os.environ.get('CALENDAR_ID')
if not CALENDAR_ID:
    try:
        import toml
        cfg = toml.load('hugo.toml')
        CALENDAR_ID = cfg.get('params', {}).get('googleCalendar', {}).get('calendarId')
    except Exception:
        CALENDAR_ID = None

if not CALENDAR_ID:
    print('Calendar ID not set. Set CALENDAR_ID env var or add params.googleCalendar.calendarId to hugo.toml')
    sys.exit(1)

# Build public ics URL
ics_url = f'https://calendar.google.com/calendar/ical/{CALENDAR_ID}/public/basic.ics'
print('Fetching', ics_url)
resp = requests.get(ics_url, timeout=20)
resp.raise_for_status()
raw = resp.text

# Very small ICS parser for VEVENTs
# We look for blocks between BEGIN:VEVENT and END:VEVENT and extract SUMMARY, DTSTART, DTEND, LOCATION, DESCRIPTION, URL
vevents = re.split(r'BEGIN:VEVENT\r?\n', raw)[1:]
events = []
now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)

for block in vevents:
    try:
        part = block.split('\nEND:VEVENT', 1)[0]
    except Exception:
        continue
    # Unfold folded lines (lines that start with space are continuation)
    lines = []
    for line in part.splitlines():
        if line.startswith(' '):
            if lines:
                lines[-1] += line[1:]
        else:
            lines.append(line)

    data = {}
    for line in lines:
        if ':' not in line:
            continue
        key, val = line.split(':', 1)
        key = key.split(';')[0]
        data.setdefault(key, val)
    summary = data.get('SUMMARY', '').strip()
    dtstart = data.get('DTSTART')
    dtend = data.get('DTEND')
    location = data.get('LOCATION', '').strip()
    description = data.get('DESCRIPTION', '').strip()
    url = data.get('URL', '').strip()

    # Parse dates - handle date or dateTime formats
    def parse_dt(v):
        if not v:
            return None
        # If it ends with Z or has T -> treat as datetime
        try:
            if re.match(r"^\d{8}T\d{6}Z?$", v):
                # e.g. 20250101T200000Z or 20250101T200000
                if v.endswith('Z'):
                    return dateparser.parse(v)
                else:
                    # naive local -> assume UTC
                    return dateparser.parse(v).replace(tzinfo=datetime.timezone.utc)
            # date-only
            if re.match(r"^\d{8}$", v):
                d = datetime.datetime.strptime(v, '%Y%m%d').date()
                # treat all-day as start at 00:00 UTC
                return datetime.datetime(d.year, d.month, d.day, tzinfo=datetime.timezone.utc)
            # fallback
            return dateparser.parse(v)
        except Exception:
            return None

    start = parse_dt(dtstart)
    end = parse_dt(dtend)
    if not start:
        continue
    # Only future events
    if start < now:
        continue
    events.append({
        'title': summary,
        'start_iso': start.isoformat(),
        'end_iso': end.isoformat() if end else None,
        'location': location,
        'description': description,
        'url': url,
    })

# Sort and limit
events = sorted(events, key=lambda e: e['start_iso'])[:DEFAULT_MAX]

# Ensure data folder exists
OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
with OUT_PATH.open('w', encoding='utf-8') as f:
    json.dump(events, f, ensure_ascii=False, indent=2)

print(f'Wrote {len(events)} events to {OUT_PATH}')
