Google Calendar integration

This document describes how to show upcoming concerts from a Google Calendar on the homepage.

1) Make the calendar public (recommended for a simple client-side widget)

- Open Google Calendar in a browser and go to Settings → Settings for my calendars → select the calendar.
- Under "Access permissions for events", check "Make available to public". This makes the calendar readable by the widget without OAuth.
- Copy the "Calendar ID" from the calendar settings (it's usually something like yourname@gmail.com or a long id).

2) Create an API key

- Go to Google Cloud Console, create or select a project.
- Enable the "Google Calendar API" for the project.
- In "APIs & Services → Credentials" create an API key. Restrict it by HTTP referrers to your domain if desired.

3) Configure your site

Add the following to `hugo.toml` (or your site params) under `[params]`:

[params.googleCalendar]
  calendarId = "your_calendar_id@group.calendar.google.com"
  apiKey = "YOUR_GOOGLE_API_KEY"

Then rebuild your site.

4) What the widget does

- Client-side JS fetches the next upcoming events (max 8) using the public Calendar API and your API key. Event titles open the event's link in a new tab; an expander shows the event notes/description inline so users can view details without leaving the page.
- If the calendar or API key is missing, the widget will fall back to either build-time `data/calendar_events.json` (if present) or the public Google iframe embed.

Serverless endpoint option (automatic updates)

- There is an optional Netlify serverless function `netlify/functions/calendar.js` that fetches the public ICS, parses it, and returns JSON. Configure it with the `CALENDAR_ID` or `CALENDAR_ICS_URL` environment variable. The function returns `Cache-Control: public, max-age=300` so the client sees updated events within ~5 minutes.
- If you deploy that function (Netlify/Vercel/AWS Lambda), set `params.googleCalendar.endpoint` in `hugo.toml` to the function URL. The homepage widget will call the endpoint and render a compact list; updates on your Google Calendar will be visible automatically and users will see the latest events without a site rebuild.

5) Private calendars


If you need to access a private calendar, you'll need a server-side proxy that performs OAuth2 and returns events to the site. That requires hosting a small serverless function or backend and is beyond this simple client-side approach. The repository includes a build-time Python script (`scripts/fetch_calendar.py`) for static builds and a Netlify function example for runtime updates.

Security and behavior notes

- API-key approach (what we implemented): quick and easy. Add your API key to `hugo.toml` under `params.googleCalendar.apiKey` (we added it for you while testing). Restrict the key by HTTP referrers to your domain and localhost during development.
- Link behavior: event titles are rendered as links (open in a new tab). Event notes are available inline via the small expander; this keeps the homepage compact while making full info accessible.
- If you prefer no client API key, use the serverless endpoint (no Google API usage) or the iframe embed fallback.

Deployment checklist

- Add the `params.googleCalendar` block to `hugo.toml` if not present: calendar ID and either `apiKey` (API approach) or `endpoint` (serverless approach).
- Optional: set up the `scripts/fetch_calendar.py` in CI to generate `data/calendar_events.json` for static builds.
- If using the API key: restrict the key in Google Cloud Console (HTTP referrers + API restriction to Google Calendar API).
- If using Netlify functions: add `CALENDAR_ID` or `CALENDAR_ICS_URL` as environment variables in Netlify site settings.

If you want, I can prepare a `netlify.toml` and a small PR that sets `params.googleCalendar.endpoint` to the deployed function URL — you'll only need to add the environment variable in your Netlify site settings.

Deployment notes for Netlify

- Place `netlify/functions/calendar.js` in the repo and add `package.json` with dependencies (`axios`, `ical`).
- Add environment variable `CALENDAR_ID` or `CALENDAR_ICS_URL` in Netlify site settings.
- Deploy the site to Netlify; the function URL will be something like `https://<your-site>.netlify.app/.netlify/functions/calendar`.
- Set `params.googleCalendar.endpoint` in `hugo.toml` to that URL.

6) Troubleshooting

- If you see a 403 or 401 error, check that the API key is valid and the Calendar API is enabled.
- If no events appear, verify the calendar is public and the calendar ID is correct.

Provided calendar details (configured for you):

- Calendar ID: `hgp3omm8735qu0ame6nj5e7boc@group.calendar.google.com`
- Public embed URL:

  https://calendar.google.com/calendar/embed?src=hgp3omm8735qu0ame6nj5e7boc%40group.calendar.google.com&ctz=Europe%2FBerlin

- Public iCal URL:

  https://calendar.google.com/calendar/ical/hgp3omm8735qu0ame6nj5e7boc%40group.calendar.google.com/public/basic.ics

Embed iframe fallback (no API key required):

<iframe src="https://calendar.google.com/calendar/embed?src=hgp3omm8735qu0ame6nj5e7boc%40group.calendar.google.com&ctz=Europe%2FBerlin" style="border: 0" width="800" height="600" frameborder="0" scrolling="no"></iframe>

Notes:
- The client-side widget (recommended) shows a compact next-events list but requires a Google API key in `params.googleCalendar.apiKey`.
- If you prefer the built-in Google embed grid/calendar, use the iframe above (already public). The iframe updates automatically from Google.
