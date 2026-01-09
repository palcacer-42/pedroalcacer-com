Concert sync: Google Calendar → Hugo site
======================================

Overview
--------

This repository now includes a server-side fetcher that reads events from a Google Calendar
and writes them to `data/concerts.json`. Hugo can render that data using the provided
shortcode `layouts/shortcodes/concerts.html`.

Quick setup
-----------

1. Create a Google API key with the Calendar API enabled (for a public calendar) or follow
   the private-calendar instructions below.
2. Add two repository secrets in GitHub: `GOOGLE_API_KEY` and `CALENDAR_ID`.
   - `CALENDAR_ID` is often your Gmail address or a calendar's ID (ending in `@group.calendar.google.com`).
3. The workflow `.github/workflows/sync_concerts.yml` will run hourly and commit
   updates to `data/concerts.json`.

Private calendars
-----------------

If your calendar is private, you have options:

- Make the calendar public (read-only) and use an API key (simple).
- Use a server-side OAuth flow or a service account that has access to the calendar. This requires
  more setup (credentials storage). See Google Calendar API docs.

Usage on the site
-----------------

Place the shortcode where you want events to appear, for example in a page template:

{{% raw %}}{{< concerts >}}{{% endraw %}}

Customization
-------------

The fetcher writes a simple JSON array with fields like `title`, `start`, `end`, `location`, `description`, and `link`.
You can extend the Python script `scripts/tools/fetch_calendar.py` to normalize fields, filter events, or
generate per-event content files under `content/` instead of a single `data/` file.

Security
--------

Store API keys and credentials as GitHub Secrets. The workflow uses the repository's `GITHUB_TOKEN` to commit changes.
