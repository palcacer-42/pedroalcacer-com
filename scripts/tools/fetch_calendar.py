#!/usr/bin/env python3
"""Fetch events from a Google Calendar (public or API-key-accessible) and write data/concerts.json

Environment variables:
  GOOGLE_API_KEY  - required for public calendars / API-key access
  CALENDAR_ID     - required (calendar identifier, e.g. your_email@gmail.com or <id>@group.calendar.google.com)
  OUTFILE         - optional, defaults to data/concerts.json

This script is intentionally simple: it uses the Google Calendar REST API with an API key.
For private calendars, see docs/concert_sync.md for options (service account / OAuth).
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote_plus

import requests


def iso_now() -> str:
    return datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()


def fetch_events(api_key: str, calendar_id: str) -> list:
    time_min = iso_now()
    url = f"https://www.googleapis.com/calendar/v3/calendars/{quote_plus(calendar_id)}/events"
    params = {
        "singleEvents": "true",
        "orderBy": "startTime",
        "timeMin": time_min,
        "maxResults": 2500,
        "key": api_key,
    }
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    items = data.get("items", [])
    events = []
    for it in items:
        start = it.get("start", {})
        end = it.get("end", {})
        start_val = start.get("dateTime") or start.get("date")
        end_val = end.get("dateTime") or end.get("date")
        event = {
            "id": it.get("id"),
            "title": it.get("summary"),
            "start": start_val,
            "end": end_val,
            "location": it.get("location"),
            "description": it.get("description"),
            "link": it.get("htmlLink"),
            "created": it.get("created"),
            "updated": it.get("updated"),
        }
        events.append(event)
    return events


def main() -> int:
    api_key = os.environ.get("GOOGLE_API_KEY")
    calendar_id = os.environ.get("CALENDAR_ID")
    outpath = Path(os.environ.get("OUTFILE", "data/concerts.json"))

    if not api_key or not calendar_id:
        print("Missing environment variables: GOOGLE_API_KEY and CALENDAR_ID are required.")
        return 2

    outpath.parent.mkdir(parents=True, exist_ok=True)

    try:
        events = fetch_events(api_key, calendar_id)
    except Exception as exc:
        print(f"Failed to fetch calendar events: {exc}")
        return 3

    # Optional: filter or normalize events here (e.g., only future events)
    with outpath.open("w", encoding="utf-8") as fh:
        json.dump(events, fh, ensure_ascii=False, indent=2)

    print(f"Wrote {outpath} ({len(events)} events)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
